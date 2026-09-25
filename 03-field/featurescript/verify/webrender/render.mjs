// Headless WebGL renders of the off-line build.
//
//   node render.mjs --model field.glb [--model more.glb ...] --shots shots.json --out DIR
//   node render.mjs --model match.glb --shots frames.json --video match.webm [--fps 24]
//
// shots.json: [{ "name": "reveal-wide", "eye": [x, y, z], "target": [x, y, z], "fov": 35,
//               "width": 1600, "height": 900, ...stage options }]   (field inches, Z up)
// Chromium comes from PLAYWRIGHT_BROWSERS_PATH (/opt/pw-browsers here) or CHROMIUM=path.
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawn } from 'node:child_process';
import { chromium } from 'playwright-core';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const opt = (k, many = false) => {
  const out = [];
  for (let i = 0; i < args.length; i++) if (args[i] === k) out.push(args[i + 1]);
  return many ? out : out[0];
};
const models = opt('--model', true).map(p => path.resolve(p));
const shots = JSON.parse(fs.readFileSync(opt('--shots'), 'utf8'));
const outDir = path.resolve(opt('--out') || '.');
fs.mkdirSync(outDir, { recursive: true });

const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.glb': 'model/gltf-binary', '.json': 'application/json' };
const server = http.createServer((req, res) => {
  const u = decodeURIComponent(req.url.split('?')[0]);
  let file;
  const m = u.match(/^\/models\/(\d+)\.glb$/);
  if (m) file = models[+m[1]];
  else file = path.join(HERE, path.normalize(u).replace(/^(\.\.[/\\])+/, ''));
  if (!file || !fs.existsSync(file) || fs.statSync(file).isDirectory()) { res.writeHead(404); res.end(); return; }
  res.writeHead(200, { 'Content-Type': TYPES[path.extname(file)] || 'application/octet-stream' });
  fs.createReadStream(file).pipe(res);
});
await new Promise(r => server.listen(0, '127.0.0.1', r));
const port = server.address().port;

// the old headless mode Playwright uses lives in chrome-headless-shell; fall back to a full Chromium
const shells = ['/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell', '/opt/pw-browsers/chromium'];
const exe = process.env.CHROMIUM || shells.find(p => fs.existsSync(p));
const browser = await chromium.launch({
  executablePath: exe,
  args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'],
});
const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
page.on('console', m => { if (m.type() === 'error') console.error('page:', m.text()); });
page.on('pageerror', e => console.error('page error:', e.message));
await page.goto(`http://127.0.0.1:${port}/stage.html`);
await page.waitForFunction(() => window.ready === true, null, { timeout: 60000 });
// --video: every shot is one frame, JPEG-piped into the VP8/WebM encoder that ships with Playwright
const video = opt('--video');
let ff = null;
if (video) {
  const ffmpeg = process.env.FFMPEG || '/opt/pw-browsers/ffmpeg-1011/ffmpeg-linux';
  ff = spawn(ffmpeg, ['-hide_banner', '-loglevel', 'error', '-y', '-f', 'image2pipe', '-c:v', 'mjpeg',
    '-framerate', String(opt('--fps') || 24), '-i', 'pipe:0', '-c:v', 'libvpx', '-b:v', opt('--bitrate') || '6M',
    '-auto-alt-ref', '0', path.resolve(video)], { stdio: ['pipe', 'inherit', 'inherit'] });
}
let n = 0;
for (const s of shots) {
  const t0 = Date.now();
  const w = s.width || 1600, h = s.height || 900;
  await page.setViewportSize({ width: w, height: h });
  await page.evaluate(o => window.stage(o), { ...s, models: models.map((_, i) => `/models/${i}.glb`) });
  if (ff) {
    const buf = await page.locator('canvas').screenshot({ type: 'jpeg', quality: 92 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (++n % 24 === 0) console.log(`frame ${n}/${shots.length}`);
  } else {
    const file = path.join(outDir, `${s.name}.png`);
    await page.locator('canvas').screenshot({ path: file });
    console.log(`${file}  ${((Date.now() - t0) / 1000).toFixed(1)} s`);
  }
}
if (ff) {
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  console.log(`wrote ${video} (${n} frames)`);
}
await browser.close();
server.close();
