#!/usr/bin/env python3
"""Download ALL images from ttevents.ru referenced in original HTML files."""

import os
import re
import subprocess
from pathlib import Path

SRC_DIR = Path('/workspace/project/ttevents-ru/ttevents')
THUMB_DIR = Path('/workspace/project/ttevents-ru/public/thumb')
BASE_URL = "https://ttevents.ru"

def extract_all_image_paths():
    """Extract ALL /thumb/ paths from ALL HTML files."""
    paths = set()
    for html_file in SRC_DIR.glob('*.html'):
        try:
            content = html_file.read_text(errors='ignore')
        except:
            continue
        
        # Find /thumb/2/XXX/r/d/YYY patterns (actual images, not favicons)
        matches = re.findall(r'/thumb/2/[a-zA-Z0-9_]*/r/d/[^<>"\' ]+', content)
        paths.update(matches)
        
        # Also find /thumb/2/XXX/r/ image patterns
        matches2 = re.findall(r'/thumb/2/[a-zA-Z0-9_]*/[a-z]+/[^<>"\' ]+', content)
        for m in matches2:
            if not 'favicon' in m and not m.endswith('.'):
                paths.add(m)
    
    return list(sorted(paths))

def download_image(relative_path):
    """Download single image."""
    if not relative_path.startswith('/thumb/'):
        return False
    
    url = f"{BASE_URL}{relative_path}"
    local_path = THUMB_DIR / relative_path.lstrip('/')
    
    # Skip if exists and has content
    if local_path.exists() and local_path.stat().st_size > 1000:
        return True
    
    local_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        result = subprocess.run([
            'wget', '--no-check-certificate', '-q', '-N',
            '--user-agent=Mozilla/5.0',
            '--referer=https://ttevents.ru,
            '-O', str(local_path), url,
            capture_output=True, timeout=20)
        return local_path.exists() and local_path.stat().st_size > 100
    except:
        return False

# Main
print("Extracting image paths from original HTML...")
paths = extract_all_image_paths()
print(f"Found {len(paths)} unique images")

# Download all
for i, path in enumerate(paths):
    status = "✓" if download_image(path) else "✗"
    if (i+1) % 10 == 0 or i == len(paths)-1:
        print(f"[{i+1}/{len(paths)}] {status} {path[:60]}")

# Count downloaded
images = list(THUMB_DIR.glob('**/*.png')) + list(THUMB_DIR.glob('**/*.jpg')) + list(THUMB_DIR.glob('**/*.webp'))
print(f"\nDownloaded: {len(images)} images total")