const DB = {};

DB.open = function (storeName) {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open('ClimateLine', 1);
    req.onupgradeneeded = e => {
      const db = e.target.result;
      if (!db.objectStoreNames.contains(storeName)) {
        db.createObjectStore(storeName, { keyPath: 'key' });
      }
    };
    req.onsuccess = e => resolve(e.target.result);
    req.onerror = e => reject(e.target.error);
  });
};

DB.get = async function (storeName, key) {
  const db = await DB.open(storeName);
  return new Promise((resolve, reject) => {
    const tx = db.transaction(storeName, 'readonly');
    const req = tx.objectStore(storeName).get(key);
    req.onsuccess = () => {
      const entry = req.result;
      if (!entry) resolve(null);
      else if (Date.now() > entry.expiresAt) resolve(null);
      else resolve(entry.data);
    };
    req.onerror = e => reject(e.target.error);
  });
};

DB.set = async function (storeName, key, data, ttlMs) {
  const db = await DB.open(storeName);
  return new Promise((resolve, reject) => {
    const tx = db.transaction(storeName, 'readwrite');
    tx.objectStore(storeName).put({
      key,
      data,
      expiresAt: Date.now() + ttlMs,
      storedAt: Date.now(),
    });
    tx.oncomplete = () => resolve();
    tx.onerror = e => reject(e.target.error);
  });
};

DB.TTL = {
  WEATHER: 30 * 60 * 1000,
  EXTREMES: 60 * 60 * 1000,
  EARTHQUAKES: 5 * 60 * 1000,
  HURRICANES: 30 * 60 * 1000,
  TRENDS: 60 * 60 * 1000,
  ALERTS: 10 * 60 * 1000,
  HISTORY: 24 * 60 * 60 * 1000,
};
