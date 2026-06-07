const USGS = {};

USGS.fetchLatest = async function (minMagnitude = 4.5) {
  const cached = await DB.get('earthquakes', 'latest');
  if (cached) return cached;

  const url = `${APP.USGS_API}?format=geojson&minmagnitude=${minMagnitude}&orderby=time&limit=20`;
  const res = await fetch(url);
  if (!res.ok) throw new Error('USGS error');
  const data = await res.json();
  const events = data.features.map(f => ({
    id: f.id,
    title: f.properties.title,
    mag: f.properties.mag,
    place: f.properties.place,
    time: new Date(f.properties.time).toISOString(),
    depth: f.geometry.coordinates[2],
    lat: f.geometry.coordinates[1],
    lon: f.geometry.coordinates[0],
    url: f.properties.url,
    type: f.properties.type || 'earthquake',
  }));

  await DB.set('earthquakes', 'latest', events, DB.TTL.EARTHQUAKES);
  return events;
};
