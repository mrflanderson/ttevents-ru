#!/usr/bin/env python3
"""Better content extraction."""

import re
from pathlib import Path
import html

SRC = Path('/workspace/project/ttevents-ru/ttevents')
OUT = Path('/workspace/project/ttevents-ru/src/pages')

def get_title(html_content):
    # og:title first
    m = re.search(r'<meta\s+property=["\']og:title["\']\s+content=["\']([^"\']+)["\']', html_content)
    if m:
        return html.unescape(m.group(1))
    # regular title
    m = re.search(r'<title>([^<]+)</title>', html_content)
    if m:
        return html.unescape(m.group(1))
    return ''

def get_desc(html_content):
    m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', html_content)
    if m:
        return html.unescape(m.group(1))
    return ''

def get_keywords(html_content):
    m = re.search(r'<meta\s+name=["\']keywords["\']\s+content=["\']([^"\']+)["\']', html_content)
    if m:
        return html.unescape(m.group(1))
    return ''

def clean_body(html_content):
    """Extract only body content, clean garbage."""
    m = re.search(r'<body[^>]*>(.+?)</body>', html_content, re.DOTALL)
    if not m:
        return ''
    content = m.group(1)
    
    # Remove scripts
    content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    
    # Remove mosaic wrappers
    content = re.sub(r'<div\s+class=["\'][^"\']*mosaic[^"\']*["\'][^>]*>.*?</div>', '', content, flags=re.DOTALL)
    content = re.sub(r'<div\s+class=["\'][^"\']*root[^"\']*["\'][^>]*>.*?</div>', '', content, flags=re.DOTALL)
    content = re.sub(r'<div\s+class=["\'][^"\']*lpc-[^"\']*["\'][^>]*>', '<div>', content)
    
    # Remove ugly attrs
    content = re.sub(r'\s+id=["\']u-[^"\']*["\']', '', content)
    content = re.sub(r'\s+data-do-[^"\']*=["\'][^"\']*["\']', '', content)
    content = re.sub(r'\s+data-elem-type=["\'][^"\']*["\']', '', content)
    content = re.sub(r'\s+data-lp-selector=["\'][^"\']*["\']', '', content)
    content = re.sub(r'\s+data-path=["\'][^"\']*["\']', '', content)
    
    # Clean up empty divs and classes
    content = re.sub(r'<div>\s*</div>', '', content)
    content = re.sub(r'\s+class=""', '', content)
    
    return content.strip()

def slug_to_filename(s):
    if s == 'index':
        return 'home.astro'
    return s + '.astro'

# Process all pages
for html_file in sorted(SRC.glob('*.html')):
    slug = html_file.stem
    
    # Skip non-content
    if slug in ['sitemap', '_']:
        continue
    
    try:
        content = html_file.read_text(errors='ignore')
    except:
        continue
    
    if len(content) < 500:
        continue
    
    title = get_title(content)
    desc = get_desc(content)
    keywords = get_keywords(content)
    body = clean_body(content)
    
    if not title:
        title = slug.replace('-', ' ').title()
    
    # Skip if content is too short
    if len(body) < 100:
        print(f"SKIP {slug}: no content")
        continue
    
    out_file = OUT / slug_to_filename(slug)
    
    # Check if exists with good content
    if out_file.exists():
        existing = out_file.read_text(errors='ignore')
        if 'page-content' in existing and len(existing) > 500:
            continue
    
    # Write
    astro = f'''---
import Layout from '../components/Layout.astro';

const pageTitle = '{title}';
const pageDescription = '{desc}';
const keywords = '{keywords}';
---

<Layout title={{pageTitle}} description={{pageDescription}} keywords={{keywords}}>
    <div class="page-content">
        <div class="container">
            {body}
        </div>
    </div>
</Layout>'''
    
    out_file.write_text(astro, errors='ignore')
    print(f"Created: {slug}")

print("Done!")