const NHC = {};

NHC.fetchActive = async function () {
  const cached = await DB.get('hurricanes', 'active');
  if (cached) return cached;

  const url = 'https://www.nhc.noaa.gov/CurrentStorms.json';
  try {
    const res = await fetch(url);
    if (!res.ok) throw new Error('NHC error');
    const data = await res.json();
    const storms = [];

    if (data?.activeStorms) {
      data.activeStorms.forEach(s => {
        if (s?.positions) {
          s.positions.forEach(p => {
            storms.push({
              name: s.name,
              basin: s.basin,
              wind: p.wind,
              pressure: p.pressure,
              lat: p.latitude,
              lon: p.longitude,
              time: p.time,
              category: s.classification,
            });
          });
        }
      });
    }

    await DB.set('hurricanes', 'active', storms, DB.TTL.HURRICANES);
    return storms;
  } catch {
    return [];
  }
};
