const OpenMeteo = {};

OpenMeteo.fetchWeather = async function (lat, lon) {
  const url = `${APP.FORECAST_API}?latitude=${lat}&longitude=${lon}&daily=temperature_2m_max,temperature_2m_min,wind_speed_10m_max,precipitation_sum,weather_code&timezone=auto&forecast_days=1`;
  const data = await OpenMeteo._fetch(url, 'weather', DB.TTL.WEATHER);
  return data.daily;
};

OpenMeteo.fetchAllExtremes = async function () {
  const lats = APP.CITIES.map(c => c.lat).join(',');
  const lons = APP.CITIES.map(c => c.lon).join(',');
  const url = `${APP.FORECAST_API}?latitude=${lats}&longitude=${lons}&daily=temperature_2m_max,temperature_2m_min,wind_speed_10m_max&timezone=auto&forecast_days=1`;

  const cached = await DB.get('extremes', 'all');
  if (cached) return cached;

  const res = await fetch(url);
  if (!res.ok) throw new Error('Extremes fetch failed');
  const data = await res.json();

  const results = data.map((d, i) => ({
    ...APP.CITIES[i],
    max: d.daily?.temperature_2m_max?.[0] ?? null,
    min: d.daily?.temperature_2m_min?.[0] ?? null,
    wind: d.daily?.wind_speed_10m_max?.[0] ?? null,
  }));

  await DB.set('extremes', 'all', results, DB.TTL.EXTREMES);
  return results;
};

OpenMeteo.fetchHistory = async function (lat, lon, startDate, endDate) {
  const key = `history_${lat}_${lon}_${startDate}_${endDate}`;
  const cached = await DB.get('history', key);
  if (cached) return cached;

  const url = `${APP.HISTORICAL_API}?latitude=${lat}&longitude=${lon}&start_date=${startDate}&end_date=${endDate}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=auto`;
  const data = await OpenMeteo._fetch(url);
  await DB.set('history', key, data.daily, DB.TTL.HISTORY);
  return data.daily;
};

OpenMeteo._fetch = async function (url, cacheStore, ttl) {
  if (cacheStore && ttl) {
    const cached = await DB.get(cacheStore, url);
    if (cached) return cached;
  }
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Open-Meteo error: ${res.status}`);
  const data = await res.json();
  if (cacheStore && ttl) await DB.set(cacheStore, url, data, ttl);
  return data;
};
