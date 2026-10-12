// Export every artboard to PNG (png/) and one multi-artboard PDF (Illustrator opens each page as an artboard).
// Usage: PW=/path/to/playwright-core/index.mjs CHROME=/path/to/chrome node export.mjs
import fs from 'fs'; import { execFileSync } from 'child_process';
const { chromium } = await import(process.env.PW || 'playwright-core');
const dir = new URL('.', import.meta.url).pathname;
const man = JSON.parse(fs.readFileSync(dir + 'manifest.json'));
fs.mkdirSync(dir + 'png', { recursive: true }); fs.mkdirSync(dir + 'pdf/_pages', { recursive: true });
const b = await chromium.launch({ executablePath: process.env.CHROME, args: ['--allow-file-access-from-files'] });
const pages = [];
for (const a of man) {
  const name = a.file.replace('svg/', '').replace('.svg', '');
  const p = await b.newPage({ viewport: { width: a.width, height: a.height } });
  await p.goto('file://' + dir + a.file); await p.waitForTimeout(400);
  await p.screenshot({ path: `${dir}png/${name}.png`, omitBackground: true });
  // 1 artboard unit = 1 pt
  await p.pdf({ path: `${dir}pdf/_pages/${name}.pdf`, width: `${a.width / 72}in`, height: `${a.height / 72}in`,
                scale: 4 / 3, printBackground: true, pageRanges: '1' });
  pages.push(`${dir}pdf/_pages/${name}.pdf`); await p.close();
}
await b.close();
execFileSync('pdfunite', [...pages, dir + 'pdf/babalas-summer-2026-all-artboards.pdf']);
fs.rmSync(dir + 'pdf/_pages', { recursive: true });
console.log(man.length, 'artboards exported');
