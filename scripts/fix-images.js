import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const rootDir = path.join(__dirname, "..", "src", "pages");
const OLD_PATTERN = "/g/s3/mosaic/images/";

// Image mappings - all scraper images to local images
const imageMap = {
  "hero-bg.jpg": "/images/lp-fon-image.png",
  "spacer.gif": "/images/tt_fav.png",
  "tt-events-logo-new.png": "/images/tt_fav.png",
  // Blog images
  "blog-3-trenda-1.jpg":
    "/images/den_semi_lyubvi_i_vernosti_v_ekaterininskom_parke_2023_ttprazdnik_2mp4_20260310_160153543_2.jpg",
  // Case images (generic fallback)
  "case.jpg": "/images/tt_fav.png",
};

function findAstroFiles(dir) {
  const files = [];
  const items = fs.readdirSync(dir, { withFileTypes: true });

  for (const item of items) {
    const fullPath = path.join(dir, item.name);
    if (item.isDirectory()) {
      files.push(...findAstroFiles(fullPath));
    } else if (item.name.endsWith(".astro") && !item.name.endsWith(".bak")) {
      files.push(fullPath);
    }
  }
  return files;
}

function fixContent(content) {
  let fixed = content;

  for (const [oldName, localPath] of Object.entries(imageMap)) {
    const pattern = `"${OLD_PATTERN}${oldName}"`;
    fixed = fixed.replace(new RegExp(pattern, "g"), `"${localPath}"`);
  }

  return fixed;
}

const astroFiles = findAstroFiles(rootDir);
let changed = 0;

for (const file of astroFiles) {
  let content = fs.readFileSync(file, "utf-8");
  const fixed = fixContent(content);

  if (content !== fixed) {
    fs.writeFileSync(file, fixed, "utf-8");
    changed++;
    console.log(`Fixed: ${file.replace(process.cwd(), ".")}`);
  }
}

console.log(`\nFixed ${changed} files`);
