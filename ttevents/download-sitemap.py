#!/usr/bin/env python3
"""
Скачивает sitemap.xml с сайта ttevents.ru
"""

import os
import ssl
import urllib.request

BASE_URL = "https://ttevents.ru"
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = True
ssl_context.verify_mode = ssl.CERT_REQUIRED

print("Downloading sitemap.xml...")

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
        import gzip as gzip_module

        if response.headers.get("Content-Encoding") == "gzip":
            content = gzip_module.decompress(content)
    except Exception:
        pass

    # Сохраняем sitemap
    sitemap_path = os.path.join(OUTPUT_DIR, "sitemap.xml")
    with open(sitemap_path, "wb") as f:
        f.write(content)

    print(f"✓ Sitemap downloaded: {len(content)} bytes")

    # Парсим URL
    import re

    urls = re.findall(r"<loc>(.*?)</loc>", content.decode("utf-8"))
    print(f"✓ Found {len(urls)} URLs in sitemap")
    print("\nFirst 10 URLs:")
    for i, url in enumerate(urls[:10]):
        print(f"  {i + 1}. {url}")

except Exception as e:
    print(f"✗ Error downloading sitemap: {e}")
