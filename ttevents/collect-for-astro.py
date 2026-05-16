#!/usr/bin/env python3
"""
Скрипт для сбора всех данных для Astro из sitemap
Скачивает страницы и собирает metadata
"""

import json
import os
import re
import ssl
import urllib.request
from datetime import datetime
from urllib.parse import urljoin, urlparse

BASE_URL = "https://ttevents.ru"
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
MAX_PAGES = 62  # Скачиваем все страницы из sitemap

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = True
ssl_context.verify_mode = ssl.CERT_REQUIRED

visited_urls = set()
pages_metadata = {}


def get_relative_path(url, base_url):
    """Получение относительного пути для сохранения файла"""
    parsed_url = urlparse(url)
    parsed_base = urlparse(base_url)
    if parsed_url.netloc != parsed_base.netloc:
        return os.path.join("external", parsed_url.netloc, parsed_url.path.lstrip("/"))
    path = parsed_url.path.lstrip("/")
    if not path or path == "/":
        path = "index.html"
    return path


def download_page(url, base_url):
    """Скачивает и сохраняет страницу"""
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept-Encoding": "gzip, deflate",
            },
        )

        response = urllib.request.urlopen(req, context=ssl_context, timeout=30)
        content = response.read()

        # Распаковываем gzip если нужно
        try:
            import gzip as gzip_module

            if response.headers.get("Content-Encoding") == "gzip":
                content = gzip_module.decompress(content)
        except Exception:
            pass

        # Сохраняем страницу
        # Извлекаем slug из URL
        parsed = urlparse(url)
        slug = parsed.path.rstrip("/").strip("/")
        if not slug or slug == "/":
            slug = "index"
        slug = slug.replace("/", "-")  # Заменяем / на -

        output_path = os.path.join(OUTPUT_DIR, slug + ".html")

        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content.decode("utf-8", errors="replace"))

        print(f"✓ Downloaded: {url}")
        return True

    except Exception as e:
        print(f"✗ Error downloading {url}: {e}")
        return False


def main():
    start_time = datetime.now()

    print("=" * 80)
    print("TT Events - Collect Pages for Astro")
    print("=" * 80)
    print(f"Sitemap: {BASE_URL}/sitemap.xml")
    print(f"Max pages: {MAX_PAGES}")
    print("=" * 80)

    # Скачиваем sitemap
    print("\n[Step 1] Downloading sitemap...")
    try:
        req = urllib.request.Request(
            f"{BASE_URL}/sitemap.xml",
            headers={"User-Agent": "Mozilla/5.0"},
        )
        response = urllib.request.urlopen(req, context=ssl_context, timeout=30)
        sitemap_content = response.read()

        try:
            import gzip as gzip_module

            if response.headers.get("Content-Encoding") == "gzip":
                sitemap_content = gzip_module.decompress(sitemap_content)
        except Exception:
            pass

        sitemap_path = os.path.join(OUTPUT_DIR, "sitemap.xml")
        with open(sitemap_path, "wb") as f:
            f.write(sitemap_content)

        print(f"✓ Sitemap downloaded: {len(sitemap_content)} bytes")

        # Парсим URL
        urls = re.findall(r"<loc>(.*?)</loc>", sitemap_content.decode("utf-8"))
        print(f"✓ Found {len(urls)} URLs in sitemap")

    except Exception as e:
        print(f"✗ Error downloading sitemap: {e}")
        return

    # Скачиваем страницы
    print("\n[Step 2] Downloading pages...")
    for i, url in enumerate(urls[:MAX_PAGES]):
        print(f"[{i + 1}/{MAX_PAGES}] {url}")
        if url not in visited_urls:
            visited_urls.add(url)
            download_page(url, BASE_URL)

        # Небольшая задержка между запросами
        import time

        time.sleep(1)

    elapsed = (datetime.now() - start_time).total_seconds()

    print("\n" + "=" * 80)
    print("COLLECTION COMPLETE")
    print("=" * 80)
    print(f"✓ Pages downloaded: {len(visited_urls)}")
    print(f"Time elapsed: {elapsed:.1f} seconds")
    print("=" * 80)
    print(f"\nSitemap saved: {sitemap_path}")
    print("\nNext steps:")
    print("  1. Run: python tools\\convert-to-astro.py")
    print("  2. Start Astro: npm run dev")


if __name__ == "__main__":
    main()
