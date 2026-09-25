// Paginate build/manual.html with Paged.js and print it, and print build/plates.html, in
// headless Chromium.  Usage: node render.mjs <manual.pdf> [<plates.pdf>]
// Chromium: $CHROME_PATH, else the browser Playwright installed (npx playwright install chromium).
// Paged.js fetches its stylesheets, so the pages are served over a local HTTP server rather
// than opened as file:// URLs.
import { chromium } from "playwright-core";
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "..", "..", "..", "..");
const TYPES = { ".html": "text/html", ".css": "text/css", ".js": "text/javascript", ".svg": "image/svg+xml",
  ".png": "image/png", ".jpg": "image/jpeg", ".woff2": "font/woff2", ".json": "application/json" };

const server = http.createServer((req, res) => {
  if (req.url === "/favicon.ico") { res.writeHead(204); res.end(); return; }
  const p = path.join(root, decodeURIComponent(new URL(req.url, "http://x").pathname));
  if (!p.startsWith(root) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) {
    res.writeHead(404); res.end(); return;
  }
  res.writeHead(200, { "Content-Type": TYPES[path.extname(p)] || "application/octet-stream" });
  fs.createReadStream(p).pipe(res);
});
await new Promise((r) => server.listen(0, "127.0.0.1", r));
const base = `http://127.0.0.1:${server.address().port}/${path.relative(root, here).split(path.sep).join("/")}/build/`;

const [manualPdf, platesPdf] = process.argv.slice(2);
const browser = await chromium.launch({ executablePath: process.env.CHROME_PATH || undefined });
const page = await browser.newPage();
page.on("console", (m) => { if (m.type() === "error" || m.type() === "warning") console.error("[page]", m.text(), m.location().url || ""); });
page.on("requestfailed", (r) => console.error("[failed]", r.url()));
page.on("response", (r) => { if (r.status() >= 400) console.error("[http]", r.status(), r.url()); });
page.on("pageerror", (e) => console.error("[page error]", e.message));

await page.goto(base + "manual.html", { waitUntil: "load" });
await page.evaluate(() => document.fonts.ready);
const pages = await page.evaluate(async () => (await window.PagedPolyfill.preview()).total);
await page.pdf({ path: manualPdf, preferCSSPageSize: true, printBackground: true });
// page numbers of the front matter, sections and subsections, for the PDF bookmarks
const outline = await page.evaluate(() => {
  const pageOf = (el) => Number(el.closest(".pagedjs_page").dataset.pageNumber);
  const items = [];
  for (const h of document.querySelectorAll(".front-h1, .opener h1, h2[id]")) {
    if (h.tagName === "H2") {
      if (items.length) items[items.length - 1].children.push({ title: h.textContent.replace(/^(\d+(\.\d+)*)/, "$1 "), page: pageOf(h) });
      continue;
    }
    const num = h.parentElement.querySelector(".opener-num");
    const title = num ? `${num.textContent}  ${h.lastChild.textContent}` : h.textContent;
    items.push({ title, page: pageOf(h), children: [] });
  }
  return items;
});
fs.writeFileSync(path.join(here, "build", "pages.json.part"), JSON.stringify({ pages, outline }));
console.log(`manual: ${pages} pages`);

if (platesPdf) {
  await page.goto(base + "plates.html", { waitUntil: "load" });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({ path: platesPdf, preferCSSPageSize: true, printBackground: true });
  console.log("plates: printed");
}
await browser.close();
server.close();
