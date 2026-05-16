#!/usr/bin/env python3
"""
Скрипт для конвертации scraped HTML в Astro страницы
Автоматически извлекает SEO данные из HTML и генерирует Astro файлы
"""

import json
import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path


class HTMLSEOParser(HTMLParser):
    """Извлекает SEO метаданные из HTML"""

    def __init__(self):
        super().__init__()
        self.title = ""
        self.meta = {}
        self.headings = []
        self._in_title = False
        self._in_h1 = False
        self._in_h2 = False
        self._in_h3 = False
        self._current_heading_level = 0
        self._current_heading_text = ""

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag == "title":
            self._in_title = True
        elif tag in ["h1", "h2", "h3"]:
            level = int(tag[1])
            self._current_heading_level = level
            self._in_h1 = level == 1
            self._in_h2 = level == 2
            self._in_h3 = level == 3
            self._current_heading_text = ""
        elif tag == "meta":
            attrs_dict = dict(attrs)
            name = attrs_dict.get("name", "").lower()
            content = attrs_dict.get("content", "")
            if name:
                self.meta[name] = content

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == "title":
            self._in_title = False
        elif tag in ["h1", "h2", "h3"]:
            if self._current_heading_text:
                level = self._current_heading_level
                self.headings.append(
                    {"level": level, "text": self._current_heading_text}
                )
            self._in_h1 = False
            self._in_h2 = False
            self._in_h3 = False
            self._current_heading_level = 0

    def handle_data(self, data):
        if self._in_title:
            self.title += data.strip()
        elif self._in_h1 or self._in_h2 or self._in_h3:
            self._current_heading_text += data.strip()

    def get_seo_data(self):
        og_tags = {}
        for key, value in self.meta.items():
            if key.startswith("og:"):
                og_key = key.split(":")[1]
                og_tags[og_key] = value
            elif key.startswith("twitter:"):
                og_key = "twitter:" + key.split(":")[1]
                og_tags[og_key] = value

        return {
            "title": self.title or "TT Events",
            "description": self.meta.get("description", ""),
            "keywords": self.meta.get("keywords", ""),
            "og_tags": og_tags,
            "headings": self.headings,
        }


def generate_astro_page(html_content, seo_data, slug):
    """
    Генерирует Astro страницу из HTML контента
    """
    # Извлекаем body контент
    body_match = re.search(r"<body[^>]*>(.*?)</body>", html_content, re.DOTALL)
    if body_match:
        body_content = body_match.group(1)
    else:
        body_content = html_content

    # Извлекаем title из HTML если не извлекли из SEO
    if not seo_data["title"]:
        title_match = re.search(r"<title>(.*?)</title>", html_content)
        if title_match:
            seo_data["title"] = title_match.group(1)

    # Генерируем frontmatter
    frontmatter = (
        """---
import {definePageMeta} from 'astro:content';
import { seo } from '@/components/SEO.astro';

const pageData = {
  title: `"""
        + seo_data["title"]
        + """`,
  description: `"""
        + seo_data["description"]
        + """`,
  keywords: `"""
        + seo_data["keywords"]
        + """`,
};

const seoMeta = {
  ogTitle: `"""
        + seo_data["og_tags"].get("title", "")
        + """`,
  ogDescription: `"""
        + seo_data["og_tags"].get("description", "")
        + """`,
  ogImage: `"""
        + seo_data["og_tags"].get("image", "")
        + """`,
};

export const pageMeta = definePageMeta(() => ({
  seo: {
    title: pageData.title,
    description: pageData.description,
    keywords: pageData.keywords,
    ogTitle: seoMeta.ogTitle,
    ogDescription: seoMeta.ogDescription,
    ogImage: seoMeta.ogImage,
  },
}));

export { pageData, seoMeta };
---

"""
    )

    # Генерируем Astro контент
    astro_template = (
        """<Layout>
  <div class="astro-wrapper">
    """
        + body_content
        + """</div>
</Layout>
"""
    )

    return frontmatter + astro_template


def main():
    """Основная функция конвертации"""

    # Пути
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    scraped_dir = os.path.join(base_dir, "ttevents")
    output_dir = os.path.join(base_dir, "src", "pages")

    # Создаем директорию если не существует
    os.makedirs(output_dir, exist_ok=True)
    print(f"Output directory: {output_dir}")

    # Находим все HTML файлы
    html_files = [f for f in os.listdir(scraped_dir) if f.endswith(".html")]

    if not html_files:
        print("⚠ No HTML files found. Run collect-for-astro.py first.")
        return

    print(f"\nFound {len(html_files)} HTML files")
    print("=" * 80)

    created_pages = 0
    errors = 0

    # Конвертируем каждый файл
    for html_file in sorted(html_files):
        html_path = os.path.join(scraped_dir, html_file)

        try:
            # Читаем HTML
            with open(html_path, "r", encoding="utf-8") as f:
                html_content = f.read()

            # Парсим SEO
            parser = HTMLSEOParser()
            parser.feed(html_content)
            seo_data = parser.get_seo_data()

            # Получаем slug из имени файла
            slug = html_file.replace(".html", "")
            if slug == "index":
                slug = "home"

            # Генерируем Astro страницу
            astro_content = generate_astro_page(html_content, seo_data, slug)

            # Сохраняем Astro файл
            output_file = os.path.join(output_dir, f"{slug}.astro")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(astro_content)

            print(f"✓ Created: {slug}.astro ({seo_data['title']})")
            created_pages += 1

        except Exception as e:
            print(f"✗ Error processing {html_file}: {e}")
            errors += 1

    print("=" * 80)
    print(f"\nConversion complete: {created_pages} pages created")
    if errors:
        print(f"Errors: {errors}")
    print("\nTo start the Astro development server:")
    print("  cd " + base_dir)
    print("  npm run dev")
    print("=" * 80)


if __name__ == "__main__":
    main()
