window.siteArticles = [];

(async () => {
  try {
    const res = await fetch('/articles.json');
    if (!res.ok) throw new Error('Failed to load articles');
    window.siteArticles = await res.json();
  } catch (err) {
    console.error('articles fetch error:', err);
  }
  document.dispatchEvent(new Event('articles-loaded'));
})();
