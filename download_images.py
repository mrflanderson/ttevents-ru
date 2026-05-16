#!/usr/bin/env python3
"""Download all images from ttevents.ru"""

import os
import re
import subprocess
from pathlib import Path
import urllib.parse

PAGES_DIR = Path('/workspace/project/ttevents-ru/src/pages')
THUMB_DIR = Path('/workspace/project/ttevents-ru/public/thumb')

def extract_image_paths():
    """Extract /thumb/ paths from all pages - more flexible."""
    paths = set()
    for page in PAGES_DIR.glob('*.astro'):
        content = page.read_text(errors='ignore')
        # Find any /thumb/ pattern
        matches = re.findall(r'/thumb/2/[^<>"\' ]+', content)
        for m in matches:
            # Only keep ones that look like images
            if m.endswith(('.jpg', '.png', '.gif', '.webp')) or '/d/' in m:
                # Cut to just image path
                parts = m.split('"')
                if parts:
                    path = parts[0]
                    if '/d/' in path:
                        paths.add(path)
    return list(paths)

def download_image(relative_path):
    """Download single image."""
    if not relative_path.startswith('/thumb/'):
        return False
    
    # Convert to URL
    url = f"https://ttevents.ru{relative_path}"
    
    # Local path
    local_path = THUMB_DIR / relative_path.lstrip('/')
    
    # Skip if already exists
    if local_path.exists() and local_path.stat().st_size > 1000:
        return True
    
    local_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Download with wget
    try:
        result = subprocess.run([
            'wget', '--no-check-certificate', '-q', '-N',
            '--user-agent=Mozilla/5.0',
            '--referer=https://ttevents.ru',
            '-O', str(local_path), url], 
            capture_output=True, timeout=15)
        return local_path.exists()
    except:
        return False

# Main
print("Extracting image paths...")
paths = extract_image_paths()
print(f"Found {len(paths)} images")

# Download first 50 for test
for i, path in enumerate(paths[:50]):
    print(f"[{i+1}/50] {path[:50]}...")
    download_image(path)

# Count downloaded
downloaded = len(list(THUMB_DIR.glob('**/*.jpg'))) + len(list(THUMB_DIR.glob('**/*.png')))
print(f"\nDownloaded: {downloaded} images")