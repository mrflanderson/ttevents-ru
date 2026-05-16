#!/usr/bin/env python3
"""Download ALL images - more complete."""

import subprocess
from pathlib import Path
import re

SRC_DIR = Path('/workspace/project/ttevents-ru/ttevents')
THUMB_DIR = Path('/workspace/project/ttevents-ru/public/thumb')
BASE_URL = "https://ttevents.ru"

def extract_all():
    paths = set()
    for html_file in SRC_DIR.glob('*.html'):
        try:
            content = html_file.read_text(errors='ignore')
        except:
            continue
        # All thumb refs except favicon
        matches = re.findall(r'/thumb/2/[^<>"\' ]+', content)
        for m in matches:
            if 'favicon' not in m:  # Skip favicons
                paths.add(m)
    return list(sorted(paths))

def download(path):
    url = BASE_URL + path
    local = THUMB_DIR / path.lstrip('/')
    if local.exists() and local.stat().st_size > 500:
        return True
    local.parent.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run(['wget', '-q', '-N', '--no-check-certificate',
            '--user-agent=Mozilla/5.0', '--referer=' + BASE_URL,
            '-O', str(local), url], timeout=20, capture_output=True)
        return local.exists() and local.stat().st_size > 100
    except:
        return False

print("Extracting all...")
paths = extract_all()
print(f"Found {len(paths)} paths")

for i, p in enumerate(paths):
    download(p)
    if (i+1) % 20 == 0:
        print(f"[{i+1}/{len(paths)}]")

imgs = len(list(THUMB_DIR.glob('**/*.png'))) + len(list(THUMB_DIR.glob('**/*.jpg'))) + len(list(THUMB_DIR.glob('**/*.webp')))
print(f"Total: {imgs} images")