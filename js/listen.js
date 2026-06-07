let articles = [];
let currentIndex = -1;
let isPlaying = false;
let audio = null;

function getArticleImg(a) {
  return a.videoId
    ? `media/articles/${a.slug}.png`
    : `media/hero/${a.slug.replace(/-/g, '_')}.png`;
}

function renderListenList() {
  const el = document.getElementById('listenList');
  if (!el) return;
  el.innerHTML = articles.map((a, i) => {
    const hasAudio = !!a.audio;
    const isActive = i === currentIndex && isPlaying;
    return `
      <div class="listen-row${isActive ? ' listen-row-active' : ''}" data-index="${i}">
        <div class="listen-thumb" style="background-image: url('${getArticleImg(a)}')">
          <div class="listen-play-overlay${hasAudio ? '' : ' listen-disabled'}">
            ${hasAudio ? '&#9654;' : ''}
          </div>
        </div>
        <div class="listen-row-info">
          <div class="listen-row-title">${a.title}</div>
          <div class="listen-row-date">${a.date}</div>
        </div>
      </div>`;
  }).join('');

  el.querySelectorAll('.listen-row').forEach(row => {
    row.addEventListener('click', () => {
      const idx = parseInt(row.dataset.index);
      const art = articles[idx];
      if (!art.audio) return;
      if (idx === currentIndex && isPlaying) {
        pauseTrack();
      } else {
        playTrack(idx);
      }
    });
  });
}

function playTrack(index) {
  goToTrack(index, true);
}

function goToTrack(index, autoPlay) {
  const art = articles[index];
  if (!art || !art.audio) return;

  if (audio) { audio.pause(); audio = null; }

  currentIndex = index;
  audio = new Audio(art.audio);
  isPlaying = false;

  document.getElementById('lpTitle').textContent = art.title;
  document.getElementById('lpPlay').innerHTML = '&#9654;';
  document.getElementById('listenPlayer').classList.add('lp-open');
  document.querySelectorAll('.listen-row').forEach(r => r.classList.remove('listen-row-active'));
  const activeRow = document.querySelector(`.listen-row[data-index="${index}"]`);
  if (activeRow) activeRow.classList.add('listen-row-active');

  audio.addEventListener('ended', () => {
    const next = currentIndex + 1;
    if (next < articles.length && articles[next].audio) {
      goToTrack(next);
    } else {
      stopTrack();
    }
  });

  audio.addEventListener('error', () => {
    stopTrack();
  });

  if (autoPlay) {
    resumePlayback();
  }
}

function resumePlayback() {
  if (!audio) return;
  audio.play().then(() => {
    isPlaying = true;
    document.getElementById('lpPlay').innerHTML = '&#9646;&#9646;';
  }).catch(() => {
    isPlaying = false;
    document.getElementById('lpPlay').innerHTML = '&#9654;';
  });
}

function pauseTrack() {
  if (audio) {
    audio.pause();
    isPlaying = false;
    document.getElementById('lpPlay').innerHTML = '&#9654;';
  }
}

function stopTrack() {
  if (audio) {
    audio.pause();
    audio = null;
  }
  isPlaying = false;
  currentIndex = -1;
  document.getElementById('lpPlay').innerHTML = '&#9654;';
  document.getElementById('listenPlayer').classList.remove('lp-open');
}

document.addEventListener('articles-loaded', () => {
  articles = (window.siteArticles || []).filter(a => a.audio);
  renderListenList();
});

document.getElementById('lpPlay')?.addEventListener('click', () => {
  if (currentIndex === -1) {
    const first = articles.findIndex(a => a.audio);
    if (first >= 0) playTrack(first);
    return;
  }
  if (isPlaying) {
    pauseTrack();
  } else if (audio) {
    resumePlayback();
  }
});

document.getElementById('lpPrev')?.addEventListener('click', () => {
  if (currentIndex <= 0) return;
  const prev = currentIndex - 1;
  if (articles[prev]?.audio) playTrack(prev);
});

document.getElementById('lpNext')?.addEventListener('click', () => {
  const next = currentIndex + 1;
  if (next < articles.length && articles[next]?.audio) playTrack(next);
});
