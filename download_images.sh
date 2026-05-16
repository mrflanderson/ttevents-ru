#!/bin/bash
# Download all images from ttevents.ru

mkdir -p /workspace/project/ttevents-ru/public/thumb
cd /workspace/project/ttevents-ru/public/thumb

# Get all image URLs from pages
grep -roh "https://ttevents\.ru/thumb/[^ \"'>]+\.(jpg|png|gif|webp)" /workspace/project/ttevents-ru/src/pages/*.astro 2>/dev/null | sort -u > /tmp/img_urls.txt

echo "Found $(wc -l < /tmp/img_urls.txt) images to download"

# Download each image
while read url; do
  path=$(echo "$url" | sed 's|https://ttevents\.ru/thumb/||')
  dir=$(dirname "$path")
  mkdir -p "$dir"
  filename=$(basename "$path")
  
  # Skip if already downloaded
  if [ -f "$path" ]; then
    continue
  fi
  
  wget --no-check-certificate -q -N --user-agent="Mozilla/5.0" --referer="https://ttevents.ru" "$url" -O "$path" 2>/dev/null
  echo "Downloaded: $filename"
done < /tmp/img_urls.txt

echo "Done! Found $(find . -type f \( -name "*.jpg" -o -name "*.png" -o -name "*.gif" -o -name "*.webp" \) | wc -l) images"