const express = require('express');
const puppeteer = require('puppeteer');

const app = express();
const PORT = process.env.PORT || 3001;

const APP_ORIGIN = process.env.APP_ORIGIN || 'http://caddy';
const LOGIN_URL = new URL('/login', APP_ORIGIN).toString();
const ADMIN_EMAIL = process.env.ADMIN_EMAIL || 'admin@example.com';
const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD || 'admin123';
const FLAG_VALUE = process.env.FLAG;
const VIEW_WAIT_MS = Number(process.env.VIEW_WAIT_MS || 8000);
const NAV_TIMEOUT_MS = Number(process.env.NAV_TIMEOUT_MS || 10000);

function buildFileUrl(file) {
  const value = String(file || '').trim();
  if (!value) throw new Error('Missing file parameter.');
  const encoded = encodeURIComponent(value);
  return `${APP_ORIGIN}/files/${encoded}`;
}


const sleep = ms => new Promise(res => setTimeout(res, ms));

async function visit(targetUrl) {
  const launchOptions = {
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--incognito'],
  };
  const executablePath = process.env.CHROMIUM_PATH || process.env.PUPPETEER_EXECUTABLE_PATH;
  if (executablePath) {
    launchOptions.executablePath = executablePath;
  }

  const browser = await puppeteer.launch(launchOptions);
  const page = await browser.newPage();
  page.setDefaultNavigationTimeout(NAV_TIMEOUT_MS);

  try {
    await page.goto(LOGIN_URL, { waitUntil: 'networkidle2' });
    await page.waitForSelector('#login-form', { timeout: NAV_TIMEOUT_MS });
    await page.type('input[name=email]', ADMIN_EMAIL, { delay: 10 });
    await page.type('input[name=password]', ADMIN_PASSWORD, { delay: 10 });

    await Promise.all([
      page.click('#login-submit'),
      page.waitForNavigation({ waitUntil: 'networkidle2' }).catch(() => {}),
    ]);

    if (FLAG_VALUE) {
      await page.setCookie({
        name: 'flag',
        value: FLAG_VALUE,
        url: APP_ORIGIN,
        httpOnly: false,
        sameSite: 'Lax',
      });
    }

    await page.goto(targetUrl, { waitUntil: 'networkidle2' });
    await sleep(VIEW_WAIT_MS)
  } finally {
    await browser.close();
  }
}

app.get('/report', (req, res) => {
  let targetUrl;
  try {
    targetUrl = buildFileUrl(req.query.file);
  } catch (err) {
    return res.status(400).json({ status: 'error', error: err.message });
  }

  console.log(`[+] Visiting ${targetUrl}`)
  // Run visit asynchronously so the API responds quickly.
  visit(targetUrl).catch((err) => {
    // eslint-disable-next-line no-console
    console.error('Bot visit failed', err);
  });

  res.json({ status: 'Bot will visit your file' });
});

app.get('*', (req, res) => {
  res.json({
    message: '/report?file=',
  });
});

app.listen(PORT, () => {
  // eslint-disable-next-line no-console
  console.log(`[+] ${process.env.ADMIN_EMAIL}|${process.env.ADMIN_PASSWORD}`)
  console.log(`Report service listening on port ${PORT}`);
});
