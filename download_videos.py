#!/usr/bin/env python3
"""Download all videos from ttevents.ru."""

import subprocess
from pathlib import Path

SRC_DIR = Path('/workspace/project/ttevents-ru/ttevents')
VIDEO_DIR = Path('/workspace/project/ttevents-ru/public/f')
BASE_URL = "https://ttevents.ru"
import re

def extract_video_paths():
    paths = set()
    for html_file in SRC_DIR.glob('*.html'):
        try:
            content = html_file.read_text(errors='ignore')
        except:
            continue
        matches = re.findall(r'/f/[^<>"\' ]+', content)
        for m in matches:
            if m.endswith(('.mp4', '.webm', '.mov')):
                paths.add(m)
    return list(sorted(paths))

def download_video(relative_path):
    url = BASE_URL + relative_path
    local_path = VIDEO_DIR / relative_path.lstrip('/f/')
    if local_path.exists() and local_path.stat().st_size > 1000:
        return True
    local_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run(['wget', '-q', '-N', '--no-check-certificate',
            '--user-agent=Mozilla/5.0', '--referer=' + BASE_URL,
            '-O', str(local_path), url], timeout=60, capture_output=True)
        return local_path.exists() and local_path.stat().st_size > 100
    except:
        return False

print("Finding videos...")
paths = extract_video_paths()
print(f"Found {len(paths)} videos")

for i, path in enumerate(paths):
    ok = download_video(path)
    print(f"[{i+1}/{len(paths)}] {'OK' if ok else 'FAIL'}: {path}")

videos = len(list(VIDEO_DIR.glob('**/*.mp4')))
print(f"Done: {videos} videos downloaded")