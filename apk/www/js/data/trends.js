const Trends = {};

Trends.fetch = async function () {
  const cached = await DB.get('trends', 'trending');
  if (cached) return cached;

  const rssUrls = [
    'https://trends.google.com/trending/rss?geo=US',
    'https://trends.google.com/trending/rss?geo=GLOBAL',
  ];

  const terms = [];
  for (const url of rssUrls) {
    try {
      const res = await fetch(`https://api.allorigins.win/raw?url=${encodeURIComponent(url)}`);
      if (!res.ok) continue;
      const text = await res.text();
      const parser = new DOMParser();
      const xml = parser.parseFromString(text, 'text/xml');
      const items = xml.querySelectorAll('item');
      items.forEach(item => {
        const title = item.querySelector('title')?.textContent;
        if (title && !terms.some(t => t.title === title)) {
          terms.push({ title, source: url.includes('GLOBAL') ? 'Global' : 'US', fetchedAt: new Date().toISOString() });
        }
      });
    } catch { continue; }
  }

  await DB.set('trends', 'trending', terms.slice(0, 20), DB.TTL.TRENDS);
  return terms.slice(0, 20);
};
