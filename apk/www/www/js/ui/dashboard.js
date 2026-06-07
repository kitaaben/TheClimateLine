const Dashboard = {
  hotCityIndex: 0,
  hotCities: null,
  globalChart: null,
};

Dashboard.render = async function () {
  const el = document.getElementById('main-content');
  const curYear = new Date().getFullYear();
  const years = [curYear - 4, curYear - 3, curYear - 2, curYear - 1, curYear];

  if (!this.hotCities) {
    try {
      const results = await OpenMeteo.fetchAllExtremes();
      this.hotCities = [...results.filter(r => r.max !== null)].sort((a, b) => b.max - a.max).slice(0, 8);
    } catch {
      this.hotCities = APP.CITIES.slice(0, 8);
    }
  }

  const city = this.hotCities[this.hotCityIndex];

  el.innerHTML = `
    <div class="animate__animated animate__fadeIn space-y-6">

      <!-- City Tabs -->
      <div>
        <div class="flex items-center justify-between mb-2">
          <h2 class="text-lg font-bold text-warning">🔥 Hot Cities</h2>
          <span class="text-xs text-base-content/50">Today's extremes</span>
        </div>
        <div role="tablist" class="tabs tabs-boxed tabs-sm bg-base-300/50 p-1 overflow-x-auto flex-nowrap">
          ${this.hotCities.map((c, i) => `
            <button role="tab" class="tab tab-sm whitespace-nowrap ${i === this.hotCityIndex ? 'tab-active' : ''}" data-ctab="${i}">${c.name}</button>
          `).join('')}
        </div>
        <div id="cityContent" class="mt-3 space-y-3">
          <div class="flex justify-center py-8"><span class="loading loading-dots loading-lg text-warning"></span></div>
        </div>
      </div>

      <!-- Divider -->
      <div class="divider text-xs text-base-content/30">EXTREMES</div>

      <!-- Coldest Section -->
      <div>
        <h3 class="text-lg font-bold text-info mb-3">❄️ Coldest Today</h3>
        <div id="coldestGrid" class="space-y-3">
          <div class="flex justify-center py-4"><span class="loading loading-spinner loading-sm text-info"></span></div>
        </div>
      </div>

      <!-- Windiest Section -->
      <div>
        <h3 class="text-lg font-bold text-accent mb-3">🌪️ Windiest Today</h3>
        <div id="windiestContent">
          <div class="flex justify-center py-4"><span class="loading loading-spinner loading-sm text-accent"></span></div>
        </div>
      </div>

      <!-- Divider -->
      <div class="divider text-xs text-base-content/30">TRENDS</div>

      <!-- Global Trend -->
      <div>
        <h3 class="text-lg font-bold text-success mb-3">🌍 Global Temperature</h3>
        <div class="card bg-base-200 border border-base-300">
          <div class="card-body p-4">
            <div class="h-48"><canvas id="globalChart"></canvas></div>
          </div>
        </div>
        <div class="card bg-base-200 border border-base-300 mt-3">
          <div class="card-body p-4">
            <h4 class="card-title text-xs mb-2">5-Year Global Average</h4>
            <div id="globalTimeline"><div class="flex justify-center py-4"><span class="loading loading-spinner loading-sm"></span></div></div>
          </div>
        </div>
      </div>
    </div>
  `;

  el.querySelectorAll('[data-ctab]').forEach(btn => {
    btn.addEventListener('click', () => {
      this.hotCityIndex = parseInt(btn.dataset.ctab);
      this.render();
    });
  });

  await Promise.all([
    this.loadCityData(years),
    this.loadColdest(),
    this.loadWindiest(),
    this.loadGlobal(years),
  ]);
};

/* ─── CITY ──────────────────────────── */

Dashboard.loadCityData = async function (years) {
  const container = document.getElementById('cityContent');
  const city = this.hotCities[this.hotCityIndex];
  const curYear = new Date().getFullYear();

  try {
    const [weather, trends] = await Promise.all([
      OpenMeteo.fetchWeather(city.lat, city.lon),
      new ClimatePredict(city).computeTrends(years, 1, 12),
    ]);

    const maxTemp = weather?.temperature_2m_max?.[0];
    const inDanger = maxTemp >= APP.THRESHOLDS.TEMP_DANGER;
    const inCritical = maxTemp >= APP.THRESHOLDS.TEMP_CRITICAL;
    const inExtreme = maxTemp >= APP.THRESHOLDS.TEMP_EXTREME;

    const impact = new ClimateImpact().evaluate(trends);
    const danger = impact.statements.find(s => s.severity === 'critical' || s.severity === 'severe');

    let html = '';

    if (inDanger && danger) {
      html += `
        <div role="alert" class="alert ${inExtreme ? 'alert-error' : 'alert-warning'} shadow-lg animate__animated animate__pulse animate__infinite">
          <span class="text-xl">${inExtreme ? '🚨' : '🟡'}</span>
          <div class="flex flex-col">
            <span class="font-bold text-sm">${inExtreme ? 'EXTREME DANGER' : 'HEAT WARNING'}</span>
            <span class="text-xs opacity-80">${danger.body}</span>
          </div>
        </div>`;
    }

    html += `
      <div class="stats shadow w-full bg-base-200 border border-base-300 stats-vertical sm:stats-horizontal">
        <div class="stat py-3">
          <div class="stat-title text-[10px]">Today's Max</div>
          <div class="stat-value ${inExtreme ? 'text-error' : inCritical ? 'text-warning' : inDanger ? 'text-orange-400' : 'text-success'} text-2xl">${Format.temp(maxTemp)}</div>
          <div class="stat-desc text-[10px]">${city.country} · #${this.hotCityIndex + 1}</div>
        </div>
        <div class="stat py-3">
          <div class="stat-title text-[10px]">5-Yr Avg</div>
          <div class="stat-value text-base-content text-xl">${Format.temp(trends.yearlyData.reduce((a, d) => a + d.avgMax, 0) / trends.yearlyData.length)}</div>
          <div class="stat-desc text-[10px] ${trends.delta > 0 ? 'text-warning' : 'text-info'}">${trends.delta > 0 ? '↑' : '↓'} ${Math.abs(trends.delta).toFixed(1)}°</div>
        </div>
        <div class="stat py-3">
          <div class="stat-title text-[10px]">Decade Trend</div>
          <div class="stat-value text-base-content text-xl">${(trends.warmingRatePerYear * 10).toFixed(2)}°</div>
          <div class="stat-desc text-[10px]">per decade</div>
        </div>
      </div>

      <div class="card bg-base-200 border border-base-300">
        <div class="card-body p-3">
          <ul class="timeline timeline-vertical timeline-compact">${trends.yearlyData.map((d, i) => {
            const isLatest = i === trends.yearlyData.length - 1;
            const maxOfAll = trends.yearlyData.reduce((m, x) => Math.max(m, x.maxTemp), 0);
            const barWidth = Math.max(20, (d.maxTemp / maxOfAll) * 100);
            const barColor = d.maxTemp >= 45 ? 'bg-error' : d.maxTemp >= 43 ? 'bg-orange-600' : d.maxTemp >= 40 ? 'bg-warning' : 'bg-success';
            return `
            <li>
              ${i < trends.yearlyData.length - 1 ? '<hr/>' : ''}
              <div class="timeline-start text-[10px] font-bold ${isLatest ? 'text-success' : 'text-base-content/50'}">${d.year}</div>
              <div class="timeline-middle" style="color:${isLatest ? '#52b788' : '#3a5a4a'}">${isLatest ? '●' : '○'}</div>
              <div class="timeline-end timeline-box bg-base-300/50 p-2 w-full">
                <div class="flex justify-between items-center text-sm">
                  <span class="font-bold ${barColor.replace('bg-', 'text-')}">${Format.temp(d.maxTemp)}</span>
                  <span class="text-[10px] text-base-content/50">avg ${Format.temp(d.avgMax)}</span>
                </div>
                <div class="w-full bg-base-300 rounded-full h-1.5 mt-1">
                  <div class="${barColor} h-1.5 rounded-full" style="width:${barWidth}%"></div>
                </div>
                <div class="flex justify-between text-[10px] text-base-content/40 mt-1">
                  <span>🔥 ${d.daysAbove(APP.THRESHOLDS.TEMP_DANGER)}d >40°</span>
                  <span>🌧️ ${Math.round(d.totalPrecip)}mm</span>
                </div>
              </div>
              <hr/>
            </li>`;}).join('')}
          </ul>
        </div>
      </div>`;

    container.innerHTML = html;
  } catch {
    container.innerHTML = '<div role="alert" class="alert alert-error text-sm">Could not load city data</div>';
  }
};

/* ─── COLDEST ──────────────────────────── */

Dashboard.loadColdest = async function () {
  const container = document.getElementById('coldestGrid');
  try {
    const results = await OpenMeteo.fetchAllExtremes();
    const items = [...results.filter(r => r.min !== null)].sort((a, b) => a.min - b.min).slice(0, 5);

    container.innerHTML = items.map((c, i) => {
      const labels = ['Pole of Cold', 'Deep Freeze', 'Ice Zone', 'Frost Zone', 'Chill Zone'];
      return `
      <div class="frosted frosted-ice p-3 relative overflow-hidden">
        <div class="absolute inset-0 pointer-events-none" style="background: radial-gradient(ellipse at 50% 0%, rgba(200,240,255,${0.08 - i * 0.015}) 0%, transparent 70%);"></div>
        <div class="flex items-center justify-between relative z-10">
          <div>
            <div class="font-bold text-sm frosted-text">${c.name}</div>
            <div class="text-[10px] text-base-content/20">${c.country}</div>
          </div>
          <div class="text-right">
            <div class="text-2xl font-extrabold text-info" style="text-shadow:0 0 20px rgba(100,200,255,0.3)">${Format.temp(c.min)}</div>
            <div class="text-[10px] text-base-content/20">feels like ${Format.temp(c.min - 5)}</div>
          </div>
        </div>
        <div class="flex gap-2 mt-1 relative z-10">
          <span class="badge badge-info badge-xs">${labels[i]}</span>
          <span class="text-[10px] text-base-content/20">lat ${c.lat.toFixed(1)}</span>
        </div>
      </div>`;
    }).join('');
  } catch {
    container.innerHTML = '<div role="alert" class="alert alert-error text-sm">Failed</div>';
  }
};

/* ─── WINDIEST ──────────────────────────── */

Dashboard.loadWindiest = async function () {
  const container = document.getElementById('windiestContent');
  try {
    const results = await OpenMeteo.fetchAllExtremes();
    const items = [...results.filter(r => r.wind !== null)].sort((a, b) => b.wind - a.wind).slice(0, 8);

    container.innerHTML = `
      <ul class="timeline timeline-vertical">${items.map((c, i) => {
        const cat = c.wind >= 117 ? { icon: '🌀', label: 'Hurricane', cls: 'text-error' }
          : c.wind >= 88 ? { icon: '🌪️', label: 'Storm', cls: 'text-warning' }
          : c.wind >= 61 ? { icon: '💨', label: 'Strong', cls: 'text-accent' }
          : { icon: '🌬️', label: 'Breezy', cls: 'text-info' };
        return `
        <li>
          ${i < items.length - 1 ? '<hr class="bg-accent/10"/>' : ''}
          <div class="timeline-start text-[10px] font-bold text-accent">#${i + 1}</div>
          <div class="timeline-middle ${cat.cls}">${cat.icon}</div>
          <div class="timeline-end timeline-box bg-base-300/30 p-2 w-full">
            <div class="flex items-center justify-between">
              <div>
                <div class="font-bold text-xs">${c.name}</div>
                <div class="text-[10px] text-base-content/30">${c.country}</div>
              </div>
              <div class="text-right">
                <div class="text-xl font-extrabold ${cat.cls}">${Format.wind(c.wind)}</div>
              </div>
            </div>
            <div class="flex gap-1 mt-1">
              <span class="badge badge-xs ${cat.cls.replace('text-', 'badge-')}">${cat.label}</span>
            </div>
          </div>
          ${i < items.length - 1 ? '<hr class="bg-accent/10"/>' : ''}
        </li>`;}).join('')}
      </ul>`;
  } catch {
    container.innerHTML = '<div role="alert" class="alert alert-error text-sm">Failed</div>';
  }
};

/* ─── GLOBAL ──────────────────────────── */

Dashboard.loadGlobal = async function (years) {
  const globalCities = [
    { name: 'New York', lat: 40.71, lon: -74.01 },
    { name: 'London', lat: 51.51, lon: -0.13 },
    { name: 'Tokyo', lat: 35.68, lon: 139.69 },
    { name: 'Nairobi', lat: -1.29, lon: 36.82 },
    { name: 'Sao Paulo', lat: -23.55, lon: -46.63 },
    { name: 'Dubai', lat: 25.20, lon: 55.27 },
    { name: 'Sydney', lat: -33.87, lon: 151.21 },
    { name: 'Moscow', lat: 55.76, lon: 37.62 },
    { name: 'Beijing', lat: 39.91, lon: 116.40 },
    { name: 'Cairo', lat: 30.04, lon: 31.24 },
  ];

  try {
    const allAverages = [];
    for (const city of globalCities) {
      const trends = await new ClimatePredict(city).computeTrends(years, 1, 12);
      allAverages.push(trends.yearlyData);
    }

    const globalYearly = years.map((year, yi) => {
      const vals = allAverages.filter(arr => arr[yi]).map(arr => arr[yi].avgMax);
      return {
        year,
        avgGlobal: vals.reduce((a, b) => a + b, 0) / vals.length,
        maxGlobal: Math.max(...allAverages.filter(arr => arr[yi]).map(arr => arr[yi].maxTemp)),
        minGlobal: Math.min(...allAverages.filter(arr => arr[yi]).map(arr => arr[yi].avgMax)),
        count: vals.length,
      };
    });

    this.renderGlobalChart(globalYearly);
    this.renderGlobalTimeline(globalYearly);
  } catch {
    document.getElementById('globalTimeline').innerHTML = '<div role="alert" class="alert alert-error text-sm">Could not load global data</div>';
  }
};

Dashboard.renderGlobalChart = function (data) {
  const ctx = document.getElementById('globalChart').getContext('2d');
  if (this.globalChart) this.globalChart.destroy();

  this.globalChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: data.map(d => d.year),
      datasets: [{
        label: 'Global Avg Max (°C)',
        data: data.map(d => Math.round(d.avgGlobal * 10) / 10),
        borderColor: '#52b788',
        backgroundColor: 'rgba(82,183,136,0.12)',
        fill: true,
        borderWidth: 3,
        pointBackgroundColor: '#52b788',
        pointRadius: 5,
        tension: 0.3,
      }],
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { labels: { color: '#95d5b2', font: { size: 11 }, boxWidth: 12 } } },
      scales: {
        x: { ticks: { color: '#52796f' }, grid: { color: '#1e3a2a' } },
        y: { ticks: { color: '#52796f' }, grid: { color: '#1e3a2a' } },
      },
    },
  });
};

Dashboard.renderGlobalTimeline = function (data) {
  const container = document.getElementById('globalTimeline');
  container.innerHTML = `
    <ul class="timeline timeline-vertical timeline-compact">${data.map((d, i) => {
      const isLatest = i === data.length - 1;
      const maxOfAll = Math.max(...data.map(x => x.avgGlobal));
      const barWidth = Math.max(15, (d.avgGlobal / maxOfAll) * 100);
      return `
      <li>
        ${i < data.length - 1 ? '<hr/>' : ''}
        <div class="timeline-start text-[10px] font-bold ${isLatest ? 'text-success' : 'text-base-content/50'}">${d.year}</div>
        <div class="timeline-middle" style="color:${isLatest ? '#52b788' : '#3a5a4a'}">${isLatest ? '●' : '○'}</div>
        <div class="timeline-end timeline-box bg-base-300/50 p-2 w-full">
          <div class="flex justify-between text-xs"><span class="font-bold text-success">${d.avgGlobal.toFixed(1)}°</span><span class="text-[10px] text-base-content/50">${d.count} cities</span></div>
          <div class="w-full bg-base-300 rounded-full h-1.5 mt-1"><div class="bg-success h-1.5 rounded-full" style="width:${barWidth}%"></div></div>
          <div class="flex justify-between text-[10px] text-base-content/40 mt-1"><span>↑ ${d.maxGlobal.toFixed(1)}°</span><span>↓ ${d.minGlobal.toFixed(1)}°</span></div>
        </div>
        ${i < data.length - 1 ? '<hr/>' : ''}
      </li>`;}).join('')}
    </ul>`;
};
