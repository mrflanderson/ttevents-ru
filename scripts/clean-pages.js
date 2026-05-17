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

function cleanContent(content) {
    // Remove Fragment set:html blocks
    const fragmentRegex = /<Fragment set:html>[\s\S]*?<\/Fragment>/g;
    let cleaned = content.replace(fragmentRegex, '');

    // Remove old migration footer
    const footerRegex = /----\s*$\n\n---\n<!--\s*TT Events.*?-->/gs;
    cleaned = cleaned.replace(footerRegex, '');

    // Remove duplicate Layout sections (keep only the first one after frontmatter)
    // Find patterns like ">>\>\>\> master\n</Layout>\n\n---\n\n---\nimport Layout
    const dupLayoutRegex = />>>>>\s*master\s*\n<\/?Layout[^>]*>\s*[\s\S]*?<\/?Layout\s*>\s*\n----\s*\n\n---\s*\n\n---\s*\nimport\s+Layout/g;
    cleaned = cleaned.replace(dupLayoutRegex, '');

    // Remove extra blank lines
    cleaned = cleaned.replace(/\n{4,}/g, '\n\n\n');

    return cleaned;
}

function fixCommonSyntaxErrors(content) {
    // Fix unterminated JSX expressions
    content = content.replace(/<\s*$/gm, '');

    // Remove trailing >>>> master markers
    content = content.replace(/>>>>>\s*master/g, '');

    return content;
}

const astroFiles = findAstroFiles(srcDir);
let fixedCount = 0;

for (const file of astroFiles) {
    const original = fs.readFileSync(file, 'utf-8');
    let cleaned = cleanContent(original);
    cleaned = fixCommonSyntaxErrors(cleaned);

    if (cleaned !== original) {
        fs.writeFileSync(file, cleaned, 'utf-8');
        fixedCount++;
        console.log(`Cleaned: ${path.relative(srcDir, file)}`);
    }
}

console.log(`\nFixed ${fixedCount} files`);
