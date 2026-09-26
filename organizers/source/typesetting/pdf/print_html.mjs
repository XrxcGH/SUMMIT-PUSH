// Print one HTML page to PDF in headless Chromium, with the page's own @page rules (size,
// margins, footer boxes).  Usage: node print_html.mjs <page.html> <out.pdf>
// Used by team_updates.sh.  Chromium: $CHROME_PATH, else the browser Playwright installed.
// The page is served over a local HTTP server rooted at the repository, so its stylesheets and
// the vendored fonts load as they do for the manual (render.mjs).
import { chromium } from "playwright-core";
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "..", "..", "..", "..");
const TYPES = { ".html": "text/html", ".css": "text/css", ".js": "text/javascript", ".svg": "image/svg+xml",
  ".png": "image/png", ".woff2": "font/woff2" };

const [htmlArg, outPdf] = process.argv.slice(2);
if (!htmlArg || !outPdf) { console.error("usage: node print_html.mjs <page.html> <out.pdf>"); process.exit(2); }
const rel = path.relative(root, path.resolve(htmlArg)).split(path.sep).join("/");

const server = http.createServer((req, res) => {
  const p = path.join(root, decodeURIComponent(new URL(req.url, "http://x").pathname));
  if (!p.startsWith(root) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); res.end(); return; }
  res.writeHead(200, { "Content-Type": TYPES[path.extname(p)] || "application/octet-stream" });
  fs.createReadStream(p).pipe(res);
});
await new Promise((r) => server.listen(0, "127.0.0.1", r));

const browser = await chromium.launch({ executablePath: process.env.CHROME_PATH || undefined });
const page = await browser.newPage();
page.on("response", (r) => { if (r.status() >= 400) console.error("[http]", r.status(), r.url()); });
await page.goto(`http://127.0.0.1:${server.address().port}/${rel}`, { waitUntil: "load" });
await page.evaluate(() => document.fonts.ready);
await page.pdf({ path: outPdf, preferCSSPageSize: true, printBackground: true, tagged: true, outline: true });
await browser.close();
server.close();
console.log(`wrote ${path.relative(root, path.resolve(outPdf)).split(path.sep).join("/")}`);
