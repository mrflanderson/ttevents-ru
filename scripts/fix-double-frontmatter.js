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

function fixDoubleFrontmatter(content) {
    // Find pattern: first --- block, then comment, then --- ---, then second import
    const regex = /^(---\s*\n[\s\S]*?\n---)(\s*\n<!--\s*TT Events.*?-->)\s*(\n---\s*\n---)(\s*\nimport\s+Layout.*?\nconst.*?=\{[^}]*\};)\n---\n(\n<Layout.*?>)/;

    const match = content.match(regex);
    if (match) {
        // Keep only the second block (the real content)
        const secondBlock = match[4];
        const layoutSection = match[6];

        // Add import if not present
        let fixed = `---\nimport Layout from "../components/Layout.astro";\n`;
        if (!secondBlock.includes('import')) {
            fixed += `import SEO from "../components/SEO.astro";\n`;
        }
        fixed += secondBlock + '\n---\n' + layoutSection;
        return fixed;
    }

    return null; // No match
}

const astroFiles = findAstroFiles(srcDir);
let fixedCount = 0;

for (const file of astroFiles) {
    const content = fs.readFileSync(file, 'utf-8');
    const fixed = fixDoubleFrontmatter(content);

    if (fixed) {
        fs.writeFileSync(file, fixed, 'utf-8');
        fixedCount++;
        console.log(`Fixed: ${path.relative(srcDir, file)}`);
    }
}

console.log(`\nFixed ${fixedCount} files`);
