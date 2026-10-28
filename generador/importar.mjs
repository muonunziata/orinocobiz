// Importación real por la pantalla de Wakoo → Exportar / importar. Uso: node importar.mjs <zip> [base]
import { createRequire } from 'module';
const { chromium } = createRequire(import.meta.url)('playwright'); // npm i playwright si no está instalado
const [,, zip, base = 'http://localhost:8080'] = process.argv;
const b = await chromium.launch(process.env.PW_CHROMIUM ? { executablePath: process.env.PW_CHROMIUM } : {});
const p = await b.newPage();
await p.goto(base + '/wp-login.php');
await p.fill('#user_login', 'admin'); await p.fill('#user_pass', 'admin');
await Promise.all([p.waitForNavigation(), p.click('#wp-submit')]);
await p.goto(base + '/wp-admin/admin.php?page=wakoo-portable');
await p.setInputFiles('input[name=wakoo_file]', zip);
await p.check('input[name=wakoo_publish]');
const t0 = Date.now();
await Promise.all([p.waitForNavigation({ timeout: 600000 }), p.click('form:has(input[name=wakoo_file]) [type=submit]')]);
const secs = ((Date.now() - t0) / 1000).toFixed(1);
const notice = await p.evaluate(() => [...document.querySelectorAll('.notice, .updated, .error')].map(n => n.innerText.trim()).join(' | '));
console.log(JSON.stringify({ secs, url: p.url(), notice }));
await b.close();
