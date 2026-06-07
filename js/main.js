// Random hero background image
const heroBg = document.getElementById('heroBg');
if (heroBg && typeof heroImages !== 'undefined' && heroImages.length > 0) {
  const randomIndex = Math.floor(Math.random() * heroImages.length);
  heroBg.style.backgroundImage = `url('${heroImages[randomIndex]}')`;
}

// ─── Video Radio Player ──────────────────────────────────
let vrVideos = [];

function openVideoRadio(videoId, title) {
  const modal = document.getElementById('videoRadio');
  document.getElementById('vrTitle').textContent = title;
  playVrTrack(videoId);
  renderVrPlaylist(videoId);
  modal.classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeVideoRadio() {
  const modal = document.getElementById('videoRadio');
  modal.classList.remove('open');
  document.getElementById('vrPlayer').innerHTML = '';
  document.body.style.overflow = '';
}

function playVrTrack(videoId) {
  document.getElementById('vrPlayer').innerHTML = `
    <iframe src="https://www.youtube-nocookie.com/embed/${videoId}?autoplay=1&rel=0&loop=1&playlist=${videoId}"
      allow="autoplay; encrypted-media" allowfullscreen></iframe>`;
  const video = vrVideos.find(v => v.id === videoId);
  if (video) document.getElementById('vrTitle').textContent = video.title;
  document.querySelectorAll('.vr-track').forEach(el => {
    el.classList.toggle('active', el.dataset.id === videoId);
  });
}

function renderVrPlaylist(activeId) {
  const el = document.getElementById('vrPlaylist');
  el.innerHTML = vrVideos.map((v, i) => `
    <div class="vr-track${v.id === activeId ? ' active' : ''}" data-id="${v.id}" onclick="playVrTrack('${v.id}')">
      <img class="vr-track-thumb" src="https://img.youtube.com/vi/${v.id}/mqdefault.jpg" alt="" loading="lazy">
      <div class="vr-track-info">
        <div class="vr-track-title">${v.title}</div>
        <div class="vr-track-num">Track ${i + 1}</div>
      </div>
      <div class="vr-track-play"></div>
    </div>`).join('');
}

// Random video cards from channel
function renderVideoGrid() {
  const videoGrid = document.getElementById('videoGrid');
  if (!videoGrid || typeof channelVideos === 'undefined' || channelVideos.length === 0) return;
  const shuffled = [...channelVideos].sort(() => Math.random() - 0.5);
  vrVideos = shuffled.slice(0, 4);
  videoGrid.innerHTML = '';
  vrVideos.forEach(v => {
    const card = document.createElement('div');
    card.className = 'featured-card video-card';
    card.tabIndex = 0;
    card.setAttribute('role', 'button');
    card.innerHTML = `
      <div class="video-thumb" style="background-image: url('https://img.youtube.com/vi/${v.id}/maxresdefault.jpg');"></div>`;
    card.addEventListener('click', () => openVideoRadio(v.id, v.title));
    card.addEventListener('keydown', e => { if (e.key === 'Enter') openVideoRadio(v.id, v.title); });
    videoGrid.appendChild(card);
  });
}

renderVideoGrid();
window.addEventListener('videos-refreshed', renderVideoGrid);

// ─── Nearby Temperatures ──────────────────────────────────
const worldCities = [
  { name: 'London', country: 'UK', lat: 51.51, lon: -0.13 },
  { name: 'Nairobi', country: 'Kenya', lat: -1.29, lon: 36.82 },
  { name: 'Tokyo', country: 'Japan', lat: 35.68, lon: 139.69 },
  { name: 'Reykjavík', country: 'Iceland', lat: 64.15, lon: -21.82 },
  { name: 'Santiago', country: 'Chile', lat: -33.46, lon: -70.65 },
  { name: 'Singapore', country: 'Singapore', lat: 1.35, lon: 103.82 },
];

function loadNearbyTemps() {
  const container = document.getElementById('extremeGrid');
  if (!container) return;

  container.innerHTML = '<div class="extreme-loading">Loading global temperatures…</div>';

  if (!navigator.geolocation) {
    fetchTemps(worldCities, 'you', container);
    return;
  }

  navigator.geolocation.getCurrentPosition(
    async (pos) => {
      let userCity = { name: 'You', country: '' };
      try {
        const r = await fetch(
          `https://nominatim.openstreetmap.org/reverse?lat=${pos.coords.latitude}&lon=${pos.coords.longitude}&format=json`,
          { headers: { 'User-Agent': 'TheClimateLine/1.0' } }
        );
        if (r.ok) {
          const d = await r.json();
          if (d.address) {
            const city = d.address.city || d.address.town || d.address.village || d.address.county || '';
            const country = d.address.country || '';
            if (city) userCity = { name: city, country };
          }
        }
      } catch {}

      const cities = [{ ...userCity, lat: pos.coords.latitude, lon: pos.coords.longitude }, ...worldCities];
      fetchTemps(cities, userCity.name, container);
    },
    () => fetchTemps(worldCities, 'you', container),
    { timeout: 10000, enableHighAccuracy: false }
  );
}

async function fetchTemps(cities, userLabel, container) {
  const lats = cities.map(c => c.lat.toFixed(2)).join(',');
  const lons = cities.map(c => c.lon.toFixed(2)).join(',');

  try {
    const res = await fetch(
      `https://api.open-meteo.com/v1/forecast?latitude=${lats}&longitude=${lons}&daily=temperature_2m_max,temperature_2m_min&timezone=auto&forecast_days=1`
    );
    if (!res.ok) throw new Error('API error');
    const data = await res.json();

    const results = data.map((d, i) => ({
      name: cities[i].name,
      country: cities[i].country,
      max: Math.round(d.daily.temperature_2m_max[0]),
    }));

    const sorted = [...results].sort((a, b) => a.max - b.max);

    container.innerHTML = `
      <div class="temp-gauge">
        <div class="temp-gauge-track">
          ${sorted.slice(0, 3).map(c => `
            <span class="temp-gauge-item">
              <span class="temp-gauge-val">${c.max}°</span>
              <span class="temp-gauge-city">${c.country ? c.name + ', ' + c.country : c.name}</span>
            </span>
          `).join('')}
          <span class="temp-gauge-divider"></span>
          ${sorted.slice(3, 6).map(h => `
            <span class="temp-gauge-item">
              <span class="temp-gauge-val">${h.max}°</span>
              <span class="temp-gauge-city">${h.country ? h.name + ', ' + h.country : h.name}</span>
            </span>
          `).join('')}
        </div>
      </div>
    `;
  } catch {
    container.innerHTML = '<div class="extreme-error">Could not load temperature data.</div>';
  }
}

loadNearbyTemps();

// ─── Audio Bar ──────────────────────────────────────────
let abArticles = [];
let abIndex = -1;
let abPlaying = false;
let abAudio = null;

function getArticleUrl(slug) {
  return `articles/${slug}.html`;
}

function getArticleImg(a) {
  return `media/articles/${a.slug}.png`;
}

function renderAudioBar() {
  abArticles = (window.siteArticles || []).filter(a => a.audio);
  const bar = document.getElementById('audioBar');
  if (!bar) return;
  if (abArticles.length === 0) {
    bar.style.display = 'none';
    return;
  }
  bar.style.display = 'flex';
  if (abIndex === -1) {
    abIndex = 0;
    document.getElementById('abTitle').textContent = abArticles[0].title;
  }
}

function abPlayTrack(index) {
  const art = abArticles[index];
  if (!art) return;
  if (abAudio) { abAudio.pause(); abAudio = null; }
  abIndex = index;
  abAudio = new Audio(art.audio);
  abAudio.addEventListener('ended', () => {
    if (abIndex + 1 < abArticles.length) {
      abPlayTrack(abIndex + 1);
    } else {
      abStopTrack();
    }
  });
  abAudio.addEventListener('error', () => abStopTrack());
  abResumePlayback();
}

function abResumePlayback() {
  if (!abAudio) return;
  abAudio.play().then(() => {
    abPlaying = true;
    document.getElementById('abTitle').textContent = abArticles[abIndex].title;
    document.getElementById('abPlay').innerHTML = '&#9646;&#9646;';
  }).catch(() => {
    abPlaying = false;
    document.getElementById('abPlay').innerHTML = '&#9654;';
  });
}

function abStopTrack() {
  if (abAudio) { abAudio.pause(); abAudio = null; }
  abPlaying = false;
  document.getElementById('abPlay').innerHTML = '&#9654;';
}

document.getElementById('abPlay')?.addEventListener('click', () => {
  if (abArticles.length === 0) return;
  if (abPlaying) {
    if (abAudio) abAudio.pause();
    abPlaying = false;
    document.getElementById('abPlay').innerHTML = '&#9654;';
  } else {
    if (abAudio) {
      abResumePlayback();
    } else if (abIndex >= 0) {
      abPlayTrack(abIndex);
    }
  }
});

document.getElementById('abPrev')?.addEventListener('click', () => {
  if (abIndex > 0) abPlayTrack(abIndex - 1);
});

document.getElementById('abNext')?.addEventListener('click', () => {
  if (abIndex + 1 < abArticles.length) abPlayTrack(abIndex + 1);
});

// ─── Articles ────────────────────────────────────────────
function renderFeaturedArticles() {
  const grid = document.querySelector('.featured-section .featured-grid');
  if (!grid) return;
  const arts = window.siteArticles || [];
  const picks = arts.slice(0, 4);
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
  if (!list) return;
  const arts = window.siteArticles || [];
  list.innerHTML = arts.map(a => `
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

// ─── New Article Indicator ─────────────────────────────
function checkNewArticles() {
  const arts = window.siteArticles || [];
  if (arts.length === 0) return;
  const newest = arts.reduce((latest, a) => {
    const d = new Date(a.date);
    return d > latest ? d : latest;
  }, new Date(0));
  const newestAudio = arts.reduce((latest, a) => {
    if (!a.audio) return latest;
    const d = new Date(a.date);
    return d > latest ? d : latest;
  }, new Date(0));
  const lastVisit = localStorage.getItem('tclLastVisit');
  if (!lastVisit || newest.getTime() > parseInt(lastVisit)) {
    const link = document.querySelector('.nav-right a[href="#updates"]');
    if (link) link.classList.add('has-updates');
  }
  if (!lastVisit || newestAudio.getTime() > parseInt(lastVisit)) {
    const link = document.querySelector('.nav-right a[href="listen.html"]');
    if (link) link.classList.add('has-updates');
  }
}

function markUpdatesSeen() {
  localStorage.setItem('tclLastVisit', Date.now().toString());
  document.querySelectorAll('.nav-right a.has-updates').forEach(el => {
    el.classList.remove('has-updates');
  });
}

document.addEventListener('click', e => {
  const link = e.target.closest('.nav-right a[href="#updates"], .nav-right a[href="listen.html"]');
  if (link) setTimeout(markUpdatesSeen, 100);
});

function initArticles() {
  if (!window.siteArticles || window.siteArticles.length === 0) return;
  renderFeaturedArticles();
  renderDirectory();
  checkNewArticles();
  renderAudioBar();
}

document.addEventListener('articles-loaded', initArticles);
