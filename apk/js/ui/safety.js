const Safety = {};

Safety.render = async function () {
  const el = document.getElementById('main-content');
  el.innerHTML = `
    <div class="animate__animated animate__fadeIn space-y-4">
      <div class="flex items-center justify-between">
        <h2 class="text-xl font-bold text-success">🛡️ Safety Advice</h2>
        <span id="safetyLocation" class="badge badge-ghost badge-sm">Detecting...</span>
      </div>
      <p class="text-xs text-base-content/50 -mt-3">Preparedness guides · Tap a card for detailed steps</p>
      <div id="safetyGrid" class="grid grid-cols-1 gap-3 mt-2">
        <div class="flex justify-center py-12"><span class="loading loading-dots loading-lg text-success"></span></div>
      </div>
    </div>
  `;

  const weather = await this.getLocalWeather();
  const conditions = this.detectConditions(weather);

  if (weather) {
    document.getElementById('safetyLocation').textContent = `${Format.temp(weather.temp)} · ${weather.city.name}`;
  } else {
    document.getElementById('safetyLocation').textContent = 'All conditions';
  }

  this.renderCards(conditions, weather);
};

Safety.getLocalWeather = async function () {
  try {
    const pos = await Geo.getCurrentPosition();
    const nearest = Geo.findNearestCity(pos.lat, pos.lon);
    const daily = await OpenMeteo.fetchWeather(nearest.city.lat, nearest.city.lon);
    return {
      temp: daily.temperature_2m_max[0],
      wind: daily.wind_speed_10m_max[0],
      precip: daily.precipitation_sum[0],
      city: nearest.city,
    };
  } catch {
    try {
      const city = APP.defaultCity;
      const daily = await OpenMeteo.fetchWeather(city.lat, city.lon);
      return {
        temp: daily.temperature_2m_max[0],
        wind: daily.wind_speed_10m_max[0],
        precip: daily.precipitation_sum[0],
        city,
      };
    } catch { return null; }
  }
};

Safety.detectConditions = function (weather) {
  const active = [];
  if (!weather) return ['heatwave', 'cold', 'storm', 'flood', 'air'];
  const t = weather.temp || 0;
  const w = weather.wind || 0;
  if (t >= APP.THRESHOLDS.TEMP_DANGER) active.push('heatwave');
  if (t <= -10) active.push('cold');
  if (w >= APP.THRESHOLDS.WIND_DANGER) active.push('storm');
  if (weather.precip > 50) active.push('flood');
  if (t >= APP.THRESHOLDS.TEMP_WARN && w < 10) active.push('air');
  if (!active.length) active.push('heatwave', 'cold', 'storm', 'flood');
  return active;
};

Safety.renderCards = function (conditions, weather) {
  const grid = document.getElementById('safetyGrid');
  const shown = new Set();

  const severityMap = {
    heatwave: weather && weather.temp >= APP.THRESHOLDS.TEMP_CRITICAL ? 'alert-error' : weather && weather.temp >= APP.THRESHOLDS.TEMP_DANGER ? 'alert-warning' : 'alert-info',
    cold: weather && weather.temp <= -10 ? 'alert-error' : 'alert-info',
    storm: weather && weather.wind >= APP.THRESHOLDS.WIND_DANGER ? 'alert-error' : 'alert-warning',
    flood: 'alert-warning',
    air: 'alert-info',
  };

  grid.innerHTML = conditions.map(key => {
    const tips = Alerts.getSafetyTips(key);
    if (!tips || shown.has(key)) return '';
    shown.add(key);

    const alertClass = severityMap[key] || 'alert-info';
    const urgency = weather
      ? (alertClass === 'alert-error' ? 'High urgency' : alertClass === 'alert-warning' ? 'Moderate' : 'Precautionary')
      : 'General guide';

    return `
      <div class="collapse collapse-plus card bg-base-200 border border-base-300">
        <input type="checkbox" class="peer" />
        <div class="collapse-title p-4 flex items-center gap-3 min-h-0">
          <span class="text-2xl">${tips.icon}</span>
          <div class="flex-1">
            <div class="font-bold text-sm">${tips.title}</div>
            <div class="flex gap-2 items-center mt-0.5">
              <span class="badge badge-ghost badge-xs">${urgency}</span>
              ${weather ? `<span class="text-[10px] text-base-content/40">${Format.temp(weather.temp)} · ${Format.wind(weather.wind)}</span>` : ''}
            </div>
          </div>
        </div>
        <div class="collapse-content">
          <div class="bg-base-300/50 rounded-lg p-3">
            <ul class="space-y-2 text-sm">
              ${tips.tips.map((t, i) => `
                <li class="flex items-start gap-2.5">
                  <span class="flex-shrink-0 w-5 h-5 rounded-full bg-success/20 text-success flex items-center justify-center text-xs font-bold">${i + 1}</span>
                  <span class="text-base-content/80">${t}</span>
                </li>
              `).join('')}
            </ul>
          </div>
          <div class="mt-3 text-[10px] text-base-content/30 flex items-center gap-2">
            <span class="freshness-dot green"></span>
            <span>Based on CDC/WHO guidelines</span>
          </div>
        </div>
      </div>
    `;
  }).join('');
};
