#!/usr/bin/env python3
"""Download ALL images from ttevents.ru."""

import subprocess
from pathlib import Path

SRC_DIR = Path('/workspace/project/ttevents-ru/ttevents')
THUMB_DIR = Path('/workspace/project/ttevents-ru/public/thumb')
BASE_URL = "https://ttevents.ru"
import re

def extract_all_image_paths():
    paths = set()
    for html_file in SRC_DIR.glob('*.html'):
        try:
            content = html_file.read_text(errors='ignore')
        except:
            continue
        matches = re.findall(r'/thumb/2/[a-zA-Z0-9_]*/r/d/[^<>"\' ]+', content)
        paths.update(matches)
    return list(sorted(paths))

def download_image(relative_path):
    url = BASE_URL + relative_path
    local_path = THUMB_DIR / relative_path.lstrip('/')
    if local_path.exists() and local_path.stat().st_size > 1000:
        return True
    local_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run(['wget', '-q', '-N', '--no-check-certificate',
            '--user-agent=Mozilla/5.0', '--referer=' + BASE_URL,
            '-O', str(local_path), url], timeout=20, capture_output=True)
        return local_path.exists() and local_path.stat().st_size > 100
    except:
        return False

print("Extracting...")
paths = extract_all_image_paths()
print(f"Found {len(paths)} images")

for i, path in enumerate(paths):
    download_image(path)
    if (i+1) % 10 == 0:
        print(f"Downloaded {i+1}/{len(paths)}")

images = len(list(THUMB_DIR.glob('**/*.png'))) + len(list(THUMB_DIR.glob('**/*.jpg')))
print(f"Done: {images} images")