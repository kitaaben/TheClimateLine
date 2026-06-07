// Auto-fetched from YouTube RSS feed; falls back to hardcoded list
const CHANNEL_ID = 'UCPzAaP4WuTcfLPPSfzQPefw';
const RSS_URL = 'https://www.youtube.com/feeds/videos.xml?channel_id=' + CHANNEL_ID;
const PROXY_URL = 'https://api.allorigins.win/raw?url=' + encodeURIComponent(RSS_URL);

const channelVideosFallback = [
  { id: '_BDRjL5KTEY', title: 'Will We Be Part of the Climate Solution?' },
  { id: 'ZtmKXRKMQQg', title: 'Act Now: Prevent Climate Catastrophe' },
  { id: 'lb7LInl5ySc', title: 'Climate Catastrophe: Time to Act Now' },
  { id: 'qmARjRAbooQ', title: 'Earth\'s Climate Crisis: Beyond 1°C' },
  { id: 'EfWw6tppOhU', title: 'The Make-or-Break Decade: Climate & Food' },
  { id: '0IWJvokCDxo', title: 'The Carbon Lockout Window' },
  { id: 'kcWbzQfbIdM', title: '4°C Catastrophe: Our Final Warning' },
  { id: 'Y8UW7yayz8c', title: 'Climate Crisis: Time to Act' },
  { id: 'hsx-2QDohnM', title: 'Climate Catastrophe in Antarctica' },
  { id: 'YTTIaRMEAI4', title: 'Arctic Meltdown: Our Final Warning' },
  { id: '5n_WBsmSW_g', title: 'Methane Emissions Threaten Our Planet' },
  { id: 'P3dJ2egqxtw', title: 'Methane Leaks: The Untold Crisis' },
];

let channelVideos = [...channelVideosFallback];

async function fetchChannelVideos() {
  try {
    const res = await fetch(PROXY_URL);
    if (!res.ok) throw new Error('HTTP ' + res.status);
    const xml = await res.text();
    const parser = new DOMParser();
    const doc = parser.parseFromString(xml, 'text/xml');
    const entries = doc.querySelectorAll('entry');
    if (entries.length === 0) throw new Error('No entries');
    channelVideos = Array.from(entries).map(entry => {
      const videoId = entry.querySelector('yt\\:videoId, videoId')?.textContent || '';
      const title = entry.querySelector('title')?.textContent || '';
      return { id: videoId, title };
    }).filter(v => v.id);
    console.log('Fetched ' + channelVideos.length + ' videos from YouTube');
  } catch (e) {
    console.warn('YouTube fetch failed, using fallback list:', e.message);
    channelVideos = [...channelVideosFallback];
  }
}

fetchChannelVideos().then(() => {
  window.dispatchEvent(new CustomEvent('videos-refreshed', { detail: channelVideos }));
});
