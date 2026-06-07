const Feed = {};

Feed.render = async function () {
  const el = document.getElementById('main-content');
  el.innerHTML = `
    <div class="animate__animated animate__fadeIn space-y-4">
      <div class="flex items-center justify-between">
        <h2 class="text-xl font-bold text-success">📰 Climate Event Feed</h2>
        <button id="refreshFeed" class="btn btn-ghost btn-sm btn-square" title="Refresh">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
        </button>
      </div>

      <div id="feedFilter" class="flex gap-2 flex-wrap">
        <button class="btn btn-xs btn-primary filter-btn active" data-filter="all">All</button>
        <button class="btn btn-xs btn-ghost filter-btn" data-filter="earthquake">🌍 Earthquakes</button>
        <button class="btn btn-xs btn-ghost filter-btn" data-filter="storm">🌀 Storms</button>
        <button class="btn btn-xs btn-ghost filter-btn" data-filter="alert">⚠️ Alerts</button>
      </div>

      <div id="feedList" class="space-y-0">
        <div class="flex justify-center py-12"><span class="loading loading-dots loading-lg text-success"></span></div>
      </div>
    </div>
  `;

  document.getElementById('refreshFeed').addEventListener('click', () => this.loadEvents());
  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.filter-btn').forEach(b => b.className = 'btn btn-xs btn-ghost filter-btn');
      btn.className = 'btn btn-xs btn-primary filter-btn active';
      this.filterFeed(btn.dataset.filter);
    });
  });

  this.allEvents = [];
  await this.loadEvents();
};

Feed.allEvents = [];

Feed.loadEvents = async function () {
  const container = document.getElementById('feedList');
  const events = [];

  try {
    const quakes = await USGS.fetchLatest();
    quakes.forEach(q => events.push({
      id: q.id, time: q.time, icon: '🌍', type: 'earthquake',
      title: q.title,
      detail: `Magnitude ${q.mag} · Depth ${Math.round(q.depth)}km · ${q.place}`,
      source: 'USGS',
      severity: q.mag >= 7 ? 'error' : q.mag >= 6 ? 'warning' : q.mag >= 5 ? 'info' : 'ghost',
      filter: 'earthquake',
    }));
  } catch {}

  try {
    const storms = await NHC.fetchActive();
    const seen = new Set();
    storms.slice(0, 15).forEach(s => {
      const key = s.name + s.time;
      if (seen.has(key)) return;
      seen.add(key);
      events.push({
        id: key, time: s.time, icon: '🌀', type: 'storm',
        title: `${s.name} — ${s.category || 'Active'}`,
        detail: `Wind: ${s.wind}kt · Pressure: ${s.pressure}mb`,
        source: 'NHC',
        severity: s.wind > 100 ? 'error' : s.wind > 60 ? 'warning' : 'info',
        filter: 'storm',
      });
    });
  } catch {}

  try {
    const alerts = await Alerts.fetchNWS();
    alerts.slice(0, 20).forEach(a => events.push({
      id: a.id, time: a.fetchedAt, icon: '⚠️', type: 'alert',
      title: a.event,
      detail: a.headline || a.area,
      source: 'NWS',
      severity: a.severity === 'Extreme' ? 'error' : a.severity === 'Severe' ? 'warning' : 'info',
      filter: 'alert',
    }));
  } catch {}

  events.sort((a, b) => new Date(b.time) - new Date(a.time));
  this.allEvents = events;

  if (!events.length) {
    container.innerHTML = '<div class="flex flex-col items-center py-12 text-base-content/50"><span class="text-4xl mb-3">📭</span><p class="text-sm">No recent events</p></div>';
    return;
  }

  this.renderEvents(events);
};

Feed.renderEvents = function (events) {
  const container = document.getElementById('feedList');
  const now = new Date();

  let lastDateLabel = '';
  container.innerHTML = events.map(e => {
    const date = new Date(e.time);
    const dateLabel = date.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' });
    const showDate = dateLabel !== lastDateLabel;
    lastDateLabel = dateLabel;

    const hoursAgo = Math.floor((now - date) / 3600000);
    const timeLabel = hoursAgo < 1 ? 'Just now' : hoursAgo < 24 ? `${hoursAgo}h ago` : dateLabel;

    return `
      ${showDate ? `<div class="text-[10px] font-bold text-base-content/30 uppercase tracking-wider pt-4 pb-1 px-1">${dateLabel}</div>` : ''}
      <div class="event-item card bg-base-200 border border-base-300 rounded-lg mb-2 hover:bg-base-300 transition-colors cursor-pointer" data-filter="${e.filter}" data-eid="${e.id}">
        <div class="card-body p-3 flex flex-row items-start gap-3">
          <div class="avatar placeholder">
            <div class="w-10 rounded-full bg-base-300">
              <span class="text-lg">${e.icon}</span>
            </div>
          </div>
          <div class="flex-1 min-w-0">
            <div class="font-semibold text-sm truncate">${e.title}</div>
            <div class="text-xs text-base-content/60 line-clamp-1">${e.detail}</div>
            <div class="flex gap-2 mt-1.5">
              <span class="badge badge-${e.severity} badge-xs gap-1">${e.source}</span>
              <span class="text-[10px] text-base-content/40">${timeLabel}</span>
            </div>
          </div>
          <span class="text-base-content/20 text-lg">›</span>
        </div>
      </div>
    `;
  }).join('');

  container.onclick = e => {
    const item = e.target.closest('.event-item');
    if (item && item.dataset.eid) this.showEventDetail(item.dataset.eid);
  };
};

Feed.filterFeed = function (filter) {
  if (filter === 'all') {
    this.renderEvents(this.allEvents);
  } else {
    this.renderEvents(this.allEvents.filter(e => e.filter === filter));
  }
};

Feed.showEventDetail = function (id) {
  const event = this.allEvents.find(e => e.id === id);
  if (!event) return;
  const modal = document.createElement('dialog');
  modal.className = 'modal modal-bottom sm:modal-middle';
  modal.innerHTML = `
    <div class="modal-box">
      <form method="dialog"><button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">✕</button></form>
      <div class="flex items-center gap-3 mb-3">
        <span class="text-3xl">${event.icon}</span>
        <div>
          <h3 class="font-bold text-lg">${event.title}</h3>
          <p class="text-sm text-base-content/60">${event.source}</p>
        </div>
      </div>
      <div class="space-y-2 text-sm">
        <div class="flex justify-between p-2 bg-base-300 rounded-lg"><span class="opacity-60">Detail</span><span>${event.detail}</span></div>
        <div class="flex justify-between p-2 bg-base-300 rounded-lg"><span class="opacity-60">Time</span><span>${new Date(event.time).toLocaleString()}</span></div>
        <div class="flex justify-between p-2 bg-base-300 rounded-lg"><span class="opacity-60">Severity</span><span class="badge badge-${event.severity} badge-sm">${event.severity}</span></div>
      </div>
    </div>
    <form method="dialog" class="modal-backdrop"><button>close</button></form>
  `;
  document.body.appendChild(modal);
  modal.showModal();
  modal.addEventListener('close', () => modal.remove());
};
