#!/usr/bin/env python3
"""Convert TTEvents HTML pages to Astro format."""

import os
import re
import html
from pathlib import Path

SRC_DIR = Path('/workspace/project/ttevents-ru/ttevents')
OUT_DIR = Path('/workspace/project/ttevents-ru/src/pages')

def extract_title(html_content):
    """Extract page title from HTML."""
    # Try og:title first, then regular title
    match = re.search(r'<meta\s+property=["\']og:title["\']\s+content=["\']([^"\']+)["\']', html_content)
    if match:
        return html.unescape(match.group(1))
    
    # Try title tag
    match = re.search(r'<title>([^<]+)</title>', html_content)
    if match:
        return html.unescape(match.group(1))
    return ''

def extract_description(html_content):
    """Extract page description."""
    match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', html_content)
    if match:
        return html.unescape(match.group(1))
    return ''

def extract_keywords(html_content):
    """Extract page keywords."""
    match = re.search(r'<meta\s+name=["\']keywords["\']\s+content=["\']([^"\']+)["\']', html_content)
    if match:
        return html.unescape(match.group(1))
    return ''

def clean_content(html_content):
    """Clean HTML content from constructor garbage."""
    # Extract main content between body tags
    match = re.search(r'<body[^>]*>(.+?)</body>', html_content, re.DOTALL)
    if not match:
        return ''
    
    content = match.group(1)
    
    # Remove scripts
    content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    
    # Remove mosaic wrapper divs
    content = re.sub(r'<div\s+class=["\'][^"\']*mosaic[^"\']*["\'][^>]*>.*?</div>', '', content, flags=re.DOTALL)
    content = re.sub(r'<div\s+class=["\'][^"\']*root[^"\']*["\'][^>]*>.*?</div>', '', content, flags=re.DOTALL)
    
    # Remove ugly IDs
    content = re.sub(r'\s+id=["\']u-[^"\']*["\']', '', content)
    content = re.sub(r'class=["\'][^"\']*--u-[^"\']*["\']', 'class=""', content)
    
    # Remove data attributes
    content = re.sub(r'\s+data-do-[^"\']*=["\'][^"\']*["\']', '', content)
    
    return content.strip()

def slug_to_filename(slug):
    """Convert slug to Astro filename."""
    if slug == 'index' or slug == '':
        return 'home.astro'
    # Remove trailing /index
    if slug.endswith('/'):
        slug = slug[:-1]
    return slug + '.astro'

def convert_page(html_path):
    """Convert a single HTML page to Astro."""
    slug = html_path.stem
    
    # Skip non-page files
    if slug.startswith('index') or slug == 'sitemap':
        return None
    
    with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
        html_content = f.read()
    
    title = extract_title(html_content)
    description = extract_description(html_content)
    keywords = extract_keywords(html_content)
    content = clean_content(html_content)
    
    if not title:
        title = slug.replace('-', ' ').title()
    
    # Build Astro frontmatter
    frontmatter = f'''---
import Layout from '../components/Layout.astro';

const pageTitle = '{title}';
const pageDescription = '{description}';
const keywords = '{keywords}';
---

<Layout title={{pageTitle}} description={{pageDescription}} keywords={{keywords}}>
    <div class="page-content">
        <div class="container">
            {content}
        </div>
    </div>
</Layout>'''
    
    return frontmatter, slug

# Main migration
print("Starting migration...")

# Get all HTML files
html_files = list(SRC_DIR.glob('*.html'))
print(f"Found {len(html_files)} HTML files")

# Convert each file
converted = 0
for html_file in html_files:
    result = convert_page(html_file)
    if not result:
        continue
    
    content, slug = result
    if not slug:
        continue
    
    # Determine output filename
    if slug == 'index':
        output_file = OUT_DIR / 'home.astro'
    else:
        output_file = OUT_DIR / f'{slug}.astro'
    
    # Skip if already exists and has good content
    if output_file.exists():
        with open(output_file, 'r') as f:
            existing = f.read()
        if 'import Layout' in existing:
            print(f"Skipping {output_file.name} - already exists")
            continue
    
    # Write the file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Created: {output_file.name}")
    converted += 1

print(f"\nDone! Created {converted} pages")