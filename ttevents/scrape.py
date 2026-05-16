#!/usr/bin/env python3
"""
Скрипт для копирования сайта ttevents.ru с подготовкой для Astro
Оптимизированная версия с поддержкой:
- Многосерверные HTTP-запросы
- Повторные попытки при ошибках
- Контроль скорости (rate limiting)
- Поддержка gzip/deflate
- Отслеживание прогресса
- Безопасное SSL-соединение
- Подготовка структуры для Astro
"""

import gzip
import html.parser
import os
import re
import ssl
import sys
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from functools import wraps
from threading import Lock
from urllib.parse import urljoin, urlparse

# Конфигурация
BASE_URL = "https://ttevents.ru"
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
MAX_DEPTH = 3  # Максимальная глубина сканирования
DELAY = 1  # Задержка между запросами в секундах
MAX_WORKERS = 5  # Максимальное количество потоков
MAX_RETRIES = 3  # Максимальное количество попыток
RETRY_DELAY = 2  # Задержка между повторными попытками
REQUEST_TIMEOUT = 30  # Таймаут запроса в секундах

# Для отслеживания посещенных URL (потокобезопасно)
visited_urls = set()
visited_lock = Lock()

# Для отслеживания прогресса
progress_lock = Lock()
processed_pages = 0
failed_pages = 0
downloaded_files = 0
skipped_files = 0

# Метаданные страниц для Astro (sitemap, SEO)
pages_metadata = {}


# Декоратор для повторных попыток
def retry(max_retries=MAX_RETRIES, delay=RETRY_DELAY):
    """Декоратор для повторных попыток выполнения функции"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries:
                        raise
                    print(
                        f"  ⚠ Attempt {attempt + 1}/{max_retries} failed: {e}. Retrying..."
                    )
                    time.sleep(delay * (attempt + 1))  # Exponential backoff

        return wrapper

    return decorator


# Декоратор для контроля скорости
rate_limiter_lock = Lock()
last_request_time = 0


def rate_limiter(delay=DELAY):
    """Декоратор для контроля частоты запросов"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            global last_request_time
            with rate_limiter_lock:
                elapsed = time.time() - last_request_time
                if elapsed < delay:
                    time.sleep(delay - elapsed)
                last_request_time = time.time()
            return func(*args, **kwargs)

        return wrapper

    return decorator


class LinkParser(html.parser.HTMLParser):
    """Парсер для извлечения ссылок из HTML"""

    def __init__(self):
        super().__init__()
        self.links = []
        self.images = []
        self.stylesheets = []
        self.scripts = []
        self.title = ""
        self.meta_description = ""
        self.meta_keywords = ""
        self.og_tags = {}
        self.h1_tags = []
        self.h2_tags = []
        self.h3_tags = []
        self.sizes = {}
        self._current_tag = None
        self._current_heading = None
        self.heading_text = ""

    def handle_starttag(self, tag, attrs):
        self._current_tag = tag
        attrs_dict = dict(attrs)

        if tag == "a" and "href" in attrs_dict:
            href = attrs_dict["href"]
            if href and not href.startswith("#") and not href.startswith("javascript:"):
                self.links.append(href)

        elif tag == "img" and "src" in attrs_dict:
            src = attrs_dict["src"]
            if src:
                self.images.append(src)
                if "alt" in attrs_dict:
                    self.sizes[src] = ("img", attrs_dict["alt"])

        elif (
            tag == "link"
            and attrs_dict.get("rel") == "stylesheet"
            and "href" in attrs_dict
        ):
            self.stylesheets.append(attrs_dict["href"])

        elif tag == "script" and "src" in attrs_dict:
            src = attrs_dict["src"]
            if src:
                self.scripts.append(src)

        elif tag == "meta":
            name = attrs_dict.get("name", "").lower()
            if name == "description":
                self.meta_description = attrs_dict.get("content", "")
            elif name == "keywords":
                self.meta_keywords = attrs_dict.get("content", "")
            elif name == "og:title":
                self.og_tags["title"] = attrs_dict.get("content", "")
            elif name == "og:description":
                self.og_tags["description"] = attrs_dict.get("content", "")
            elif name == "og:image":
                self.og_tags["image"] = attrs_dict.get("content", "")

        elif tag in ["h1", "h2", "h3"]:
            self._current_heading = tag
            self.heading_text = ""
            if tag == "h1":
                self.h1_tags.append({"tag": tag, "text": ""})
            elif tag == "h2":
                self.h2_tags.append({"tag": tag, "text": ""})
            elif tag == "h3":
                self.h3_tags.append({"tag": tag, "text": ""})

    def handle_endtag(self, tag):
        if (
            tag in ["h1", "h2", "h3"]
            and self._current_heading == tag
            and self.heading_text
        ):
            if tag == "h1":
                self.h1_tags[-1]["text"] = self.heading_text
            elif tag == "h2":
                self.h2_tags[-1]["text"] = self.heading_text
            elif tag == "h3":
                self.h3_tags[-1]["text"] = self.heading_text
            self._current_heading = None
        self._current_tag = None

    def handle_data(self, data):
        """Извлекаем данные из тегов"""
        if self._current_tag == "title":
            self.title = data.strip()
        elif self._current_heading and self.heading_text is not None:
            self.heading_text += data.strip()


def normalize_url(url, base_url):
    """Нормализация URL для использования в качестве ключа"""
    parsed = urlparse(url)
    if not parsed.scheme:
        url = urljoin(base_url, url)
        parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"


def get_relative_path(url, base_url):
    """Получение относительного пути для сохранения файла"""
    parsed_url = urlparse(url)
    parsed_base = urlparse(base_url)

    if parsed_url.netloc != parsed_base.netloc:
        return os.path.join("external", parsed_url.netloc, parsed_url.path.lstrip("/"))

    path = parsed_url.path.lstrip("/")
    # Если path пустой или только слеш, используем index.html
    if not path or path == "/":
        path = "index.html"
    return path


@retry(max_retries=MAX_RETRIES, delay=RETRY_DELAY)
def rate_limited_download(url, output_path, base_url):
    """Скачивание файла с повторными попытками, rate limiting и поддержкой gzip"""
    global downloaded_files, skipped_files

    try:
        full_url = urljoin(base_url, url)
        parsed = urlparse(full_url)

        # Создаем директорию если не существует
        output_dir = os.path.dirname(output_path)
        if output_dir and output_dir != OUTPUT_DIR:
            os.makedirs(output_dir, exist_ok=True)
        elif output_dir == OUTPUT_DIR:
            os.makedirs(output_dir, exist_ok=True)

        # Проверяем размер файла (пропускаем очень большие - >10MB)
        req = urllib.request.Request(
            full_url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
            },
        )

        response = urllib.request.urlopen(
            req, context=ssl_context, timeout=REQUEST_TIMEOUT
        )
        content = response.read()

        # Распаковываем gzip если нужно
        try:
            import gzip as gzip_module
            import io

            if response.headers.get("Content-Encoding") == "gzip":
                content = gzip_module.decompress(content)
        except Exception:
            pass

        # Пропускаем большие файлы
        max_size = 10 * 1024 * 1024  # 10 MB
        if len(content) > max_size:
            with progress_lock:
                skipped_files += 1
            print(f"  ⊘ Пропущен (большой файл): {url} ({len(content)} bytes)")
            return False

        # Сохраняем файл
        with open(output_path, "wb") as f:
            f.write(content)

        with progress_lock:
            downloaded_files += 1
        print(f"  ✓ {output_path} ({len(content)} bytes)")
        return True

    except Exception as e:
        print(f"  ✗ Ошибка при скачивании {url}: {e}")
        raise  # Re-raise for retry decorator


# Alias for backward compatibility
download_file = rate_limited_download


@rate_limiter(delay=DELAY)
def process_page(url, base_url, depth=0):
    """Обработка страницы: скачивание и извлечение ссылок"""
    global processed_pages, failed_pages

    if depth > MAX_DEPTH or url in visited_urls:
        return

    with visited_lock:
        if url in visited_urls:
            return
        visited_urls.add(url)

    print(f"\n{'  ' * depth}Processing: {url}")

    try:
        # Скачиваем страницу
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept-Encoding": "gzip, deflate",
            },
        )
        response = urllib.request.urlopen(
            req, context=ssl_context, timeout=REQUEST_TIMEOUT
        )

        html_content = response.read()

        # Распаковываем gzip если нужно
        try:
            if response.headers.get("Content-Encoding") == "gzip":
                import gzip as gzip_module
                import io

                html_content = gzip_module.decompress(html_content)
        except Exception:
            pass

        html_content = html_content.decode("utf-8")

        # Парсим HTML
        parser = LinkParser()
        parser.feed(html_content)

        # Сохраняем страницу
        rel_path = get_relative_path(url, base_url)
        output_path = os.path.join(OUTPUT_DIR, rel_path)

        output_dir = os.path.dirname(output_path)
        if output_dir and output_dir != OUTPUT_DIR:
            os.makedirs(output_dir, exist_ok=True)
        elif output_dir == OUTPUT_DIR:
            os.makedirs(output_dir, exist_ok=True)

        # Создаем metadata для Astro
        pages_metadata[url] = {
            "path": rel_path,
            "title": parser.title,
            "description": parser.meta_description,
            "keywords": parser.meta_keywords,
            "og_tags": parser.og_tags,
            "h1": parser.h1_tags,
            "h2": parser.h2_tags,
            "h3": parser.h3_tags,
            "links": len(parser.links),
            "images": len(parser.images),
        }

        with open(output_path, "w", encoding="utf-8") as f:
            # Заменяем абсолютные URL на относительные для локальной навигации
            local_html = replace_urls(html_content, base_url, url)
            f.write(local_html)

        print(f"{'  ' * depth}✓ Saved: {output_path}")

        with progress_lock:
            processed_pages += 1

        # Скачиваем ресурсы параллельно
        all_resources = parser.images + parser.stylesheets + parser.scripts
        if all_resources:
            with ThreadPoolExecutor(
                max_workers=min(MAX_WORKERS, len(all_resources))
            ) as executor:
                futures = []
                for resource in all_resources:
                    resource_url = urljoin(url, resource)
                    resource_rel_path = get_relative_path(resource_url, base_url)
                    resource_path = os.path.join(OUTPUT_DIR, resource_rel_path)
                    if resource_path:
                        futures.append(
                            executor.submit(
                                download_file, resource_url, resource_path, base_url
                            )
                        )

                # Ожидаем завершения и собираем результаты
                for future in as_completed(futures):
                    try:
                        future.result()
                    except Exception as e:
                        print(f"  ✗ Error downloading resource: {e}")

        # Рекурсивно обрабатываем ссылки
        for link in parser.links:
            link_url = urljoin(url, link)
            if link_url.startswith(base_url) or (
                link_url.startswith("http")
                and urlparse(link_url).netloc == urlparse(base_url).netloc
            ):
                norm_link = normalize_url(link_url, base_url)
                if norm_link not in visited_urls:
                    process_page(norm_link, base_url, depth + 1)

    except Exception as e:
        print(f"{'  ' * depth}✗ Error processing {url}: {e}")
        with progress_lock:
            failed_pages += 1


def replace_urls(html_content, base_url, current_url):
    """Заменяет абсолютные URL на относительные для локальной навигации"""
    parsed_base = urlparse(base_url)
    parsed_current = urlparse(current_url)

    # Заменяем ссылки на другие страницы
    def replace_link(match):
        full_tag = match.group(0)
        href_match = re.search(r'href=["\']([^"\']*)["\']', full_tag)
        if not href_match:
            return full_tag

        href = href_match.group(1)
        if href.startswith("#") or href.startswith("javascript:"):
            return full_tag

        full_url = urljoin(current_url, href)
        parsed_href = urlparse(full_url)

        # Если ссылка внутри того же домена, делаем относительной
        if parsed_href.netloc == parsed_base.netloc:
            rel_path = parsed_href.path.lstrip("/")
            return re.sub(r'href=["\'][^"\']*["\']', f'href="{rel_path}"', full_tag)
        else:
            return full_tag

    # Обрабатываем href атрибуты
    html_content = re.sub(
        r'<a[^>]*href=["\'][^"\']*["\'][^>]*>', replace_link, html_content
    )

    # Заменяем src атрибуты для ресурсов
    def replace_src(match):
        full_tag = match.group(0)
        src_match = re.search(r'src=["\']([^"\']*)["\']', full_tag)
        if not src_match:
            return full_tag

        src = src_match.group(1)
        if src.startswith("data:") or src.startswith("blob:"):
            return full_tag

        full_url = urljoin(current_url, src)
        parsed_src = urlparse(full_url)

        if parsed_src.netloc == parsed_base.netloc:
            rel_path = parsed_src.path.lstrip("/")
            return re.sub(r'src=["\'][^"\']*["\']', f'src="{rel_path}"', full_tag)
        else:
            return full_tag

    html_content = re.sub(
        r'<(?:img|script|source)[^>]*src=["\'][^"\']*["\'][^>]*>',
        replace_src,
        html_content,
    )

    return html_content


def save_astro_metadata():
    """Сохраняет metadata для Astro (sitemap, SEO)"""
    import json

    # Создаем sitemap.xml
    sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    for url, metadata in pages_metadata.items():
        sitemap_content += f"<url>\n"
        sitemap_content += f"  <loc>{url}</loc>\n"
        sitemap_content += (
            f"  <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>\n"
        )
        sitemap_content += f"</url>\n"

    sitemap_content += "</urlset>\n"

    sitemap_path = os.path.join(OUTPUT_DIR, "sitemap.xml")
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(sitemap_content)

    print(f"\n📝 Sitemap saved: {sitemap_path}")

    # Сохраняем SEO metadata
    seo_path = os.path.join(OUTPUT_DIR, "seo-metadata.json")
    with open(seo_path, "w", encoding="utf-8") as f:
        json.dump(pages_metadata, f, ensure_ascii=False, indent=2)

    print(f"📝 SEO metadata saved: {seo_path}")


if __name__ == "__main__":
    import ssl

    def download_sitemap():
        """Скачивает sitemap.xml напрямую с сайта"""
        try:
            req = urllib.request.Request(
                f"{BASE_URL}/sitemap.xml",
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Accept-Encoding": "gzip, deflate",
                },
            )

            response = urllib.request.urlopen(req, context=ssl_context, timeout=30)
            content = response.read()

            # Распаковываем gzip если нужно
            try:
                if response.headers.get("Content-Encoding") == "gzip":
                    import gzip as gzip_module

                    content = gzip_module.decompress(content)
            except Exception:
                pass

            # Сохраняем sitemap
            sitemap_path = os.path.join(OUTPUT_DIR, "sitemap.xml")
            with open(sitemap_path, "wb") as f:
                f.write(content)

            print(f"✓ Sitemap downloaded: {len(content)} bytes")
            return content

        except Exception as e:
            print(f"✗ Error downloading sitemap: {e}")
            return None

    def main():
        import time as time_module

        start_time = time_module.time()

        # Создание SSL контекста для HTTPS
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = True
        ssl_context.verify_mode = ssl.CERT_REQUIRED

        print("=" * 80)
        print("TT Events Website Scraper (Optimized for Astro)")
        print("=" * 80)
        print(f"Base URL: {BASE_URL}")
        print(f"Output directory: {OUTPUT_DIR}")
        print(f"Max depth: {MAX_DEPTH}")
        print(f"Max workers: {MAX_WORKERS}")
        print(f"Max retries: {MAX_RETRIES}")
        print(f"Request timeout: {REQUEST_TIMEOUT}s")
        print("=" * 80)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)

        # 1. Скачиваем sitemap напрямую
        print("\n[Step 1] Downloading sitemap...")
        download_sitemap()

        # 2. Парсим sitemap и добавляем URL в visited_urls
        print("\n[Step 2] Parsing sitemap...")
        sitemap_path = os.path.join(OUTPUT_DIR, "sitemap.xml")
        try:
            with open(sitemap_path, "r", encoding="utf-8") as f:
                sitemap_content = f.read()

            # Извлекаем все URL из sitemap
            import re

            urls = re.findall(r"<loc>(.*?)</loc>", sitemap_content)
            print(f"Found {len(urls)} URLs in sitemap")

            # Добавляем первые несколько URL в очередь
            for url in urls[:50]:  # Ограничиваем 50 страниц
                if url not in visited_urls:
                    visited_urls.add(url)
        except Exception as e:
            print(f"⚠ Error parsing sitemap: {e}")

        # 3. Начинаем скрейпинг с главной страницы
        print("\n[Step 3] Starting crawl...")
        main_url = urljoin(BASE_URL, "/")
        process_page(main_url, BASE_URL)

        # 4. Обрабатываем оставшиеся URL из sitemap
        print("\n[Step 4] Processing sitemap URLs...")
        try:
            with open(sitemap_path, "r", encoding="utf-8") as f:
                sitemap_content = f.read()
            urls = re.findall(r"<loc>(.*?)</loc>", sitemap_content)

            for url in urls:
                if url not in visited_urls:
                    visited_urls.add(url)
                    process_page(url, BASE_URL, depth=1)
        except Exception as e:
            print(f"⚠ Error processing sitemap URLs: {e}")

        elapsed = time_module.time() - start_time

        # Сохраняем metadata для Astro
        save_astro_metadata()

        print("\n" + "=" * 80)
        print("SCRAPING COMPLETE")
        print("=" * 80)
        print(f"✓ Pages processed: {processed_pages}")
        print(f"✗ Pages failed: {failed_pages}")
        print(f"✓ Files downloaded: {downloaded_files}")
        print(f"⊘ Files skipped: {skipped_files}")
        print(f"Total URLs visited: {len(visited_urls)}")
        print(f"Time elapsed: {elapsed:.1f} seconds")
        print(f"\nFiles saved to: {OUTPUT_DIR}")
        print("=" * 80)

        # Report if there were failures
        if failed_pages > 0:
            print(f"\n⚠ Warning: {failed_pages} page(s) failed to process.")
            print("You may need to run the script again to complete the scrape.")
