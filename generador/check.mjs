// Usage: node check.mjs <url> [shot.png] [width] [full]
import { createRequire } from 'module';
const { chromium } = createRequire(import.meta.url)('playwright'); // npm i playwright si no está instalado
const [,, url, out, w='1440', full='1'] = process.argv;
const b = await chromium.launch(process.env.PW_CHROMIUM ? { executablePath: process.env.PW_CHROMIUM } : {});
const p = await b.newPage({ viewport: { width: +w, height: 900 } });
const errs = [], fails = [], ext = [];
p.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });
p.on('pageerror', e => errs.push('pageerror: ' + e.message));
p.on('requestfailed', r => fails.push(r.url() + ' ' + (r.failure()?.errorText || '')));
p.on('response', r => { if (r.status() >= 400) fails.push(r.status() + ' ' + r.url()); });
p.on('request', r => { const u = new URL(r.url()); if (!['127.0.0.1', 'localhost'].includes(u.hostname) && !u.protocol.startsWith('data')) ext.push(r.url()); });
await p.goto(url, { waitUntil: 'networkidle' });
await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 300) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 130)); } window.scrollTo(0, 0); });
await p.waitForLoadState('networkidle'); await p.waitForTimeout(1200);
const broken = await p.evaluate(() => [...document.images].filter(i => i.complete && i.naturalWidth === 0).map(i => i.src));
if (out) await p.screenshot({ path: out, fullPage: full === '1' });
console.log(JSON.stringify({ url, errs, fails, ext: [...new Set(ext)], broken }, null, 0));
await b.close();
