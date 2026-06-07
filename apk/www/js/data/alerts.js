const Alerts = {};

Alerts.fetchNWS = async function () {
  const cached = await DB.get('alerts', 'active');
  if (cached) return cached;

  const url = `${APP.NWS_API}/alerts/active?limit=20`;
  try {
    const res = await fetch(url, { headers: { 'User-Agent': '(TheClimateLine, contact@theclimateline.org)' } });
    if (!res.ok) throw new Error('NWS error');
    const data = await res.json();
    const alerts = (data.features || []).map(f => ({
      id: f.properties.id,
      headline: f.properties.headline,
      severity: f.properties.severity,
      urgency: f.properties.urgency,
      event: f.properties.event,
      area: f.properties.areaDesc,
      lat: f.geometry?.coordinates?.[1],
      lon: f.geometry?.coordinates?.[0],
      expires: f.properties.expires,
      fetchedAt: new Date().toISOString(),
    }));
    await DB.set('alerts', 'active', alerts, DB.TTL.ALERTS);
    return alerts;
  } catch { return []; }
};

Alerts.getSafetyTips = function (condition) {
  const tips = {
    heatwave: {
      icon: '🔥',
      title: 'Extreme Heat',
      tips: ['Stay indoors during peak heat (11AM-4PM)', 'Drink water every 20 minutes', 'Never leave people or pets in cars', 'Use fans or wet cloths to cool down', 'Check on elderly and vulnerable neighbors'],
    },
    cold: {
      icon: '❄️',
      title: 'Extreme Cold',
      tips: ['Layer clothing — thermal, wool, windproof', 'Protect extremities: hands, feet, ears', 'Keep moving to generate body heat', 'Never use stoves or grills indoors', 'Watch for frostbite: numbness, pale skin'],
    },
    storm: {
      icon: '🌪️',
      title: 'Severe Storm',
      tips: ['Move to the lowest floor, interior room', 'Stay away from windows and doors', 'Charge devices while power is available', 'Fill water containers', 'Have flashlight and batteries ready'],
    },
    flood: {
      icon: '🌊',
      title: 'Flood Risk',
      tips: ['Move to higher ground immediately', 'Never walk or drive through floodwater', 'Turn off electricity if flooding is imminent', 'Secure important documents in waterproof bags', 'Follow evacuation orders without delay'],
    },
    air: {
      icon: '😷',
      title: 'Poor Air Quality',
      tips: ['Wear N95 or KN95 mask outdoors', 'Keep windows and doors sealed', 'Run air purifier if available', 'Limit outdoor exercise', 'Watch for coughing, throat irritation, shortness of breath'],
    },
  };
  return tips[condition] || null;
};
