// Random hero background image
const heroBg = document.getElementById('heroBg');
if (heroBg && typeof heroImages !== 'undefined' && heroImages.length > 0) {
  const randomIndex = Math.floor(Math.random() * heroImages.length);
  heroBg.style.backgroundImage = `url('${heroImages[randomIndex]}')`;
}

// Random video cards from channel
const videoGrid = document.getElementById('videoGrid');
if (videoGrid && typeof channelVideos !== 'undefined' && channelVideos.length > 0) {
  const shuffled = [...channelVideos].sort(() => Math.random() - 0.5);
  const picks = shuffled.slice(0, 4);

  picks.forEach(v => {
    const card = document.createElement('a');
    card.href = `https://www.youtube.com/watch?v=${v.id}`;
    card.className = 'featured-card video-card';
    card.target = '_blank';
    card.rel = 'noopener';
    card.innerHTML = `
      <div class="featured-img" style="background-image: url('https://img.youtube.com/vi/${v.id}/maxresdefault.jpg');"></div>
      <div class="featured-body">
        <h3>${v.title}</h3>
        <p>Watch now on The Climate Line →</p>
      </div>`;
    videoGrid.appendChild(card);
  });
}

// ─── Extreme Temperatures ──────────────────────────────────
const extremeLocations = [
  { name: 'Death Valley', country: 'USA', lat: 36.46, lon: -116.87 },
  { name: 'Ahvaz', country: 'Iran', lat: 31.32, lon: 48.67 },
  { name: 'Jeddah', country: 'Saudi Arabia', lat: 21.54, lon: 39.17 },
  { name: 'Bangkok', country: 'Thailand', lat: 13.76, lon: 100.50 },
  { name: 'Delhi', country: 'India', lat: 28.61, lon: 77.23 },
  { name: 'Timbuktu', country: 'Mali', lat: 16.77, lon: -3.01 },
  { name: 'Dubai', country: 'UAE', lat: 25.20, lon: 55.27 },
  { name: 'Cairo', country: 'Egypt', lat: 30.04, lon: 31.24 },
  { name: 'Hermosillo', country: 'Mexico', lat: 29.07, lon: -110.96 },
  { name: 'Alice Springs', country: 'Australia', lat: -23.70, lon: 133.88 },
  { name: 'Yakutsk', country: 'Russia', lat: 62.03, lon: 129.73 },
  { name: 'Ulaanbaatar', country: 'Mongolia', lat: 47.92, lon: 106.92 },
  { name: 'Yellowknife', country: 'Canada', lat: 62.45, lon: -114.37 },
  { name: 'Nuuk', country: 'Greenland', lat: 64.18, lon: -51.72 },
  { name: 'Murmansk', country: 'Russia', lat: 68.97, lon: 33.08 },
  { name: 'Reykjavik', country: 'Iceland', lat: 64.15, lon: -21.95 },
  { name: 'Helsinki', country: 'Finland', lat: 60.17, lon: 24.94 },
  { name: 'Utqiaġvik', country: 'USA', lat: 71.29, lon: -156.79 },
  { name: 'McMurdo', country: 'Antarctica', lat: -77.85, lon: 166.67 },
  { name: 'Punta Arenas', country: 'Chile', lat: -53.16, lon: -70.91 },
];

async function loadExtremeTemps() {
  const container = document.getElementById('extremeGrid');
  if (!container) return;

  const lats = extremeLocations.map(l => l.lat).join(',');
  const lons = extremeLocations.map(l => l.lon).join(',');

  try {
    const res = await fetch(
      `https://api.open-meteo.com/v1/forecast?latitude=${lats}&longitude=${lons}&daily=temperature_2m_max,temperature_2m_min&timezone=auto&forecast_days=1`
    );
    if (!res.ok) throw new Error('API error');
    const data = await res.json();

    const results = data.map((d, i) => ({
      ...extremeLocations[i],
      max: Math.round(d.daily.temperature_2m_max[0]),
      min: Math.round(d.daily.temperature_2m_min[0]),
    }));

    const hottest = [...results].sort((a, b) => b.max - a.max).slice(0, 5);
    const coldest = [...results].sort((a, b) => a.min - b.min).slice(0, 5);

    container.innerHTML = `
      <div class="extreme-label">Temperatures</div>
      <div class="extreme-bar"></div>
      <div class="extreme-row">
        <div class="extreme-group">
          ${hottest.map(l => `
            <div class="extreme-box">
              <span class="extreme-value hot">${l.max}°</span>
              <span class="extreme-place">${l.name}</span>
            </div>
          `).join('')}
        </div>
        <div class="extreme-group">
          ${coldest.map(l => `
            <div class="extreme-box">
              <span class="extreme-value cold">${l.min}°</span>
              <span class="extreme-place">${l.name}</span>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  } catch {
    container.innerHTML = '<div class="extreme-error">Could not load temperature data.</div>';
  }
}

loadExtremeTemps();

// ─── Articles ────────────────────────────────────────────
function getArticleUrl(slug) {
  return `articles/${slug}.html`;
}

function getArticleImg(a) {
  return a.videoId
    ? `media/articles/${a.slug}.png`
    : `media/hero/${a.slug.replace(/-/g, '_')}.png`;
}

function renderFeaturedArticles() {
  const grid = document.querySelector('.featured-section .featured-grid');
  if (!grid || typeof siteArticles === 'undefined') return;

  const videoArticles = siteArticles.filter(a => a.videoId);
  const picks = videoArticles.slice(0, 4);

  grid.innerHTML = picks.map(a => `
    <a href="${getArticleUrl(a.slug)}" class="featured-card">
      <div class="featured-img" style="background-image: url('${getArticleImg(a)}');"></div>
      <div class="featured-body">
        <h3>${a.title}</h3>
        <p>${a.summary}</p>
      </div>
    </a>
  `).join('');
}

function renderDirectory() {
  const list = document.querySelector('.directory-list');
  if (!list || typeof siteArticles === 'undefined') return;

  list.innerHTML = siteArticles.map(a => `
    <a href="${getArticleUrl(a.slug)}" class="directory-row">
      <div class="dir-thumb" style="background-image: url('${getArticleImg(a)}');"></div>
      <div class="dir-content">
        <h3>${a.title}</h3>
        <p>${a.summary}</p>
      </div>
      <div class="dir-arrow">→</div>
    </a>
  `).join('');
}

renderFeaturedArticles();
renderDirectory();
