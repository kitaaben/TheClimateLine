const Format = {};

Format.temp = function (celsius) {
  return `${Math.round(celsius)}°`;
};

Format.tempWithSign = function (celsius) {
  const v = Math.round(celsius);
  return v > 0 ? `+${v}°` : `${v}°`;
};

Format.timeAgo = function (isoString) {
  const seconds = Math.floor((Date.now() - new Date(isoString).getTime()) / 1000);
  if (seconds < 60) return 'just now';
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  return `${days}d ago`;
};

Format.date = function (isoString) {
  return new Date(isoString).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
};

Format.time = function (isoString) {
  return new Date(isoString).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
};

Format.dateShort = function (isoString) {
  return new Date(isoString).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
};

Format.magnitude = function (mag) {
  if (mag >= 7) return { label: 'Major', color: 'text-error', class: 'badge-error' };
  if (mag >= 6) return { label: 'Strong', color: 'text-warning', class: 'badge-warning' };
  if (mag >= 5) return { label: 'Moderate', color: 'text-info', class: 'badge-info' };
  return { label: 'Minor', color: 'text-success', class: 'badge-ghost' };
};

Format.wind = function (kmh) {
  return `${Math.round(kmh)} km/h`;
};

Format.precip = function (mm) {
  return `${mm.toFixed(1)} mm`;
};
