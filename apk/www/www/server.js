const http = require('http');
const https = require('https');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const dir = 'C:\\TheClimateLine\\apk';
const cacheDir = path.join(dir, 'cache');
if (!fs.existsSync(cacheDir)) fs.mkdirSync(cacheDir);

function fetchUrl(url) {
  return new Promise((resolve, reject) => {
    const mod = url.startsWith('https') ? https : http;
    mod.get(url, { headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' } }, res => {
      let d = '';
      res.on('data', c => d += c);
      res.on('end', () => resolve(d));
    }).on('error', reject);
  });
}

http.createServer((req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  if (req.method === 'OPTIONS') { res.writeHead(204); return res.end(); }
  if (req.method === 'POST' && req.url === '/save') {
    let body = '';
    req.on('data', c => body += c);
    req.on('end', () => {
      try {
        const p = JSON.parse(body);
        const key = p.key;
        if (!key) { res.writeHead(400); return res.end('{"error":"Missing key"}'); }
        const hash = crypto.createHash('md5').update(key).digest('hex');
        fs.writeFileSync(path.join(cacheDir, hash + '.json'), JSON.stringify(p.data));
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end('{"ok":true}');
      } catch (e) { res.writeHead(400); res.end(JSON.stringify({ error: e.message })); }
    });
    return;
  }
  if (req.method === 'GET' && req.url.startsWith('/news?q=')) {
    const query = decodeURIComponent(req.url.split('?q=')[1] || '').split('&')[0];
    const rssUrl = 'https://news.google.com/rss/search?q=' + encodeURIComponent(query) + '&hl=en-US&gl=US&ceid=US:en';
    fetchUrl(rssUrl).then(xml => {
      const items = [];
      const itemRe = /<item>([\s\S]*?)<\/item>/g;
      let m;
      while ((m = itemRe.exec(xml)) !== null) {
        const body = m[1];
        const title = (body.match(/<title>([^<]*)<\/title>/) || ['',''])[1];
        const link = (body.match(/<link>([^<]*)<\/link>/) || ['',''])[1];
        const pubDate = (body.match(/<pubDate>([^<]*)<\/pubDate>/) || ['',''])[1];
        const source = (body.match(/<source[^>]*>([^<]*)<\/source>/) || ['',''])[1];
        const desc = (body.match(/<description>([^<]*)<\/description>/) || ['',''])[1];
        if (title) items.push({ title, link, pubDate, source, description: desc.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'") });
      }
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(items.slice(0, 10)));
    }).catch(e => {
      res.writeHead(500, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: e.message }));
    });
    return;
  }
  if (req.method === 'GET' && req.url === '/site-data') {
    const base = 'https://theclimateline.pages.dev/';
    Promise.all(['js/articles.js', 'js/channel-videos.js'].map(f => fetchUrl(base + f))).then(([articles, videos]) => {
      const aMatch = articles.match(/const\s+siteArticles\s*=\s*(\[[\s\S]*?\]);/);
      const vMatch = videos.match(/const\s+channelVideos\s*=\s*(\[[\s\S]*?\]);/);
      if (!aMatch || !vMatch) { res.writeHead(502); return res.end('{"error":"Parse failed"}'); }
      const aData = new Function('return ' + aMatch[1] + ';')();
      const vData = new Function('return ' + vMatch[1] + ';')();
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ articles: aData, videos: vData }));
    }).catch(e => { res.writeHead(500); res.end(JSON.stringify({ error: e.message })); });
    return;
  }
  var urlPath = req.url.split('?')[0];
  const file = urlPath === '/' ? 'splash.html' : urlPath.slice(1);
  const full = path.join(dir, file);
  if (!full.startsWith(dir)) { res.writeHead(403); res.end(); return; }
  fs.readFile(full, (err, data) => {
    if (err) { res.writeHead(404); res.end(); return; }
    const ext = path.extname(file);
    const ct = ext === '.css' ? 'text/css' : ext === '.js' ? 'application/javascript' : ext === '.json' ? 'application/json' : 'text/html';
    res.writeHead(200, { 'Content-Type': ct });
    res.end(data);
  });
}).listen(8080, () => console.log('Serving on http://localhost:8080'));
