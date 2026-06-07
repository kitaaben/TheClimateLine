const MapView = {
  map: null,
  markers: [],
};

MapView.render = async function () {
  const el = document.getElementById('main-content');
  el.innerHTML = `
    <div class="animate__animated animate__fadeIn flex flex-col gap-2 h-full">
      <div class="flex items-center justify-between">
        <h2 class="text-lg font-bold text-success">🗺️ Climate Map</h2>
        <div class="flex gap-2 items-center">
          <span id="mapEventCount" class="badge badge-ghost badge-sm">0 events</span>
          <span id="mapLoading" class="loading loading-spinner loading-xs text-success"></span>
        </div>
      </div>

      <div class="flex gap-1 flex-wrap mb-1">
        <button class="btn btn-xs btn-primary map-filter active" data-mfilter="all">All</button>
        <button class="btn btn-xs btn-ghost map-filter" data-mfilter="heat">🔥 Heat</button>
        <button class="btn btn-xs btn-ghost map-filter" data-mfilter="cold">❄️ Cold</button>
        <button class="btn btn-xs btn-ghost map-filter" data-mfilter="quake">🌍 Quakes</button>
      </div>

      <div id="mapContainer" class="map-container flex-1"></div>

      <div id="mapLegend" class="flex gap-4 text-[10px] text-base-content/50 justify-center pb-1">
        <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-[#c0392b]"></span> Hot</span>
        <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-[#3498db]"></span> Cold</span>
        <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-[#e67e22]"></span> Quake</span>
      </div>
    </div>
  `;

  document.querySelectorAll('.map-filter').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.map-filter').forEach(b => b.className = 'btn btn-xs btn-ghost map-filter');
      btn.className = 'btn btn-xs btn-primary map-filter active';
      this.filterMarkers(btn.dataset.mfilter);
    });
  });

  this.map = L.map('mapContainer', { zoomControl: false }).setView([20, 0], 2);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap',
    maxZoom: 18,
  }).addTo(this.map);
  L.control.zoom({ position: 'bottomright' }).addTo(this.map);

  await this.loadEvents();
  document.getElementById('mapLoading').classList.add('hidden');
  setTimeout(() => this.map.invalidateSize(), 300);
};

MapView.allMarkers = [];

MapView.loadEvents = async function () {
  const allEvents = [];

  try {
    const results = await OpenMeteo.fetchAllExtremes();
    const valid = results.filter(r => r.max !== null);
    const hottest = [...valid].sort((a, b) => b.max - a.max).slice(0, 15);
    const coldest = [...valid].sort((a, b) => a.min - b.min).slice(0, 15);

    hottest.forEach(c => allEvents.push({
      lat: c.lat, lon: c.lon, type: 'heat',
      icon: '🔥', title: `${c.name}: ${Format.temp(c.max)}`,
      detail: `Hottest today · ${c.country}`,
      color: '#c0392b',
      radius: Math.min(14, 6 + c.max / 8),
    }));

    coldest.forEach(c => allEvents.push({
      lat: c.lat, lon: c.lon, type: 'cold',
      icon: '❄️', title: `${c.name}: ${Format.temp(c.min)}`,
      detail: `Coldest today · ${c.country}`,
      color: '#3498db',
      radius: Math.min(14, 6 + Math.abs(c.min) / 8),
    }));
  } catch {}

  try {
    const quakes = await USGS.fetchLatest(4.5);
    quakes.slice(0, 30).forEach(q => allEvents.push({
      lat: q.lat, lon: q.lon, type: 'quake',
      icon: '🌍', title: `M${q.mag} · ${q.place}`,
      detail: `${Format.timeAgo(q.time)} · Depth ${Math.round(q.depth)}km`,
      color: q.mag >= 6 ? '#c0392b' : '#e67e22',
      radius: Math.min(14, 4 + q.mag * 1.5),
    }));
  } catch {}

  document.getElementById('mapEventCount').textContent = `${allEvents.length} events`;
  this.allMarkers = [];

  allEvents.forEach(e => {
    const marker = L.circleMarker([e.lat, e.lon], {
      radius: e.radius, color: e.color, fillColor: e.color, fillOpacity: 0.7, weight: 2,
    }).addTo(this.map);
    marker._climateType = e.type;
    marker.bindPopup(`
      <div style="font-family:system-ui;min-width:140px">
        <div style="font-size:18px;margin-bottom:4px">${e.icon} <b>${e.title}</b></div>
        <div style="font-size:12px;color:#666">${e.detail}</div>
      </div>
    `);
    this.allMarkers.push(marker);
  });
};

MapView.filterMarkers = function (filter) {
  this.allMarkers.forEach(m => {
    if (filter === 'all' || m._climateType === filter) {
      this.map.addLayer(m);
    } else {
      this.map.removeLayer(m);
    }
  });
};
