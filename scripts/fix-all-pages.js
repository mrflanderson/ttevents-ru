import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const srcDir = path.join(__dirname, '..', 'src', 'pages');

function findAstroFiles(dir) {
    const files = [];
    const items = fs.readdirSync(dir, { withFileTypes: true });
    for (const item of items) {
        const fullPath = path.join(dir, item.name);
        if (item.isDirectory()) {
            files.push(...findAstroFiles(fullPath));
        } else if (item.name.endsWith('.astro') && !item.name.endsWith('.bak')) {
            files.push(fullPath);
        }
    }
    return files;
}

function fixFile(content, filename) {
    // Remove any "export const pageMeta = definePageMeta..." blocks
    content = content.replace(/export const pageMeta.*?\}\);/gs, '');

    // Remove >> markers
    content = content.replace(/>\s*>/g, '');

    // Find and remove old first layout section (before the real one)
    // Pattern: first --- block, then Layout section with empty container, then --- ---
    const firstSectionRegex = /^(---\s*\nimport\s+Layout[^\n]*\nconst[^\n]*\n---\n<Layout[^>]*>[\s\S]*?<\/Layout>[\s\S]*?\n----\n\n---\s*\n\n---)/;

    // Check if file has the old pattern
    if (content.match(firstSectionRegex)) {
        const match = content.match(firstSectionRegex);
        if (match) {
            // Get everything after the old pattern
            const rest = content.substring(match[0].length);
            // Clean up leading dashes and comments
            let cleaned = rest.replace(/^\n----\s*\n\n---\s*\n<!--[\s\S]*?-->/, '\n---\n');
            return cleaned;
        }
    }

    // Check for "<Layout> <div class=\"page-content\"> <div class=\"container\"> </div> </div> </Layout>" pattern
    const emptyLayoutRegex = /<Layout[^>]*>[\s\S]*?<div class="page-content">[\s\S]*?<div class="container">\s*<\/div>[\s\S]*?<\/div>[\s\S]*?<\/Layout>/;
    if (content.match(emptyLayoutRegex)) {
        const match = content.match(emptyLayoutRegex);
        if (match) {
            // Replace with placeholder
            const placeholder = '<!-- Content to be added -->';
            content = content.replace(emptyLayoutRegex, placeholder);
        }
    }

    // Remove trailing comments
    content = content.replace(/\n---\s*\n<!--\s*TT Events.*?-->/g, '');

    // Remove extra newlines
    content = content.replace(/\n{4,}/g, '\n\n\n');

    return content;
}

const astroFiles = findAstroFiles(srcDir);
let fixedCount = 0;

for (const file of astroFiles) {
    const original = fs.readFileSync(file, 'utf-8');
    const filename = path.basename(file);
    const fixed = fixFile(original, filename);

    if (fixed !== original) {
        fs.writeFileSync(file, fixed, 'utf-8');
        fixedCount++;
        console.log(`Fixed: ${filename}`);
    }
}

console.log(`\nFixed ${fixedCount} files`);
