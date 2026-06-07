const Geo = {};

Geo.distance = function (lat1, lon1, lat2, lon2) {
  const R = 6371;
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a = Math.sin(dLat / 2) ** 2 + Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * Math.sin(dLon / 2) ** 2;
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
};

Geo.findNearestCity = function (lat, lon) {
  let nearest = null;
  let minDist = Infinity;
  for (const c of APP.CITIES) {
    const d = Geo.distance(lat, lon, c.lat, c.lon);
    if (d < minDist) {
      minDist = d;
      nearest = c;
    }
  }
  return { city: nearest, distanceKm: Math.round(minDist) };
};

Geo.getCurrentPosition = function () {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) reject(new Error('Geolocation not supported'));
    navigator.geolocation.getCurrentPosition(
      pos => resolve({ lat: pos.coords.latitude, lon: pos.coords.longitude }),
      err => reject(err),
      { timeout: 10000, enableHighAccuracy: false }
    );
  });
};
