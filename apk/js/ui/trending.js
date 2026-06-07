const Trending = {};

Trending.render = async function () {
  const el = document.getElementById('main-content');
  el.innerHTML = `
    <div class="animate__animated animate__fadeIn space-y-4">
      <div class="flex items-center justify-between">
        <h2 class="text-xl font-bold text-success">📈 Trending Searches</h2>
        <button id="refreshTrends" class="btn btn-ghost btn-sm btn-square">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
        </button>
      </div>
      <p class="text-xs text-base-content/50 -mt-3">What the world is searching about climate right now</p>
      <div id="trendList" class="space-y-0">
        <div class="flex justify-center py-12"><span class="loading loading-dots loading-lg text-success"></span></div>
      </div>
    </div>
  `;
  document.getElementById('refreshTrends').addEventListener('click', () => this.loadTrends());
  await this.loadTrends();
};

Trending.loadTrends = async function () {
  const container = document.getElementById('trendList');
  try {
    const terms = await Trends.fetch();
    if (!terms.length) throw new Error('Empty');

    container.innerHTML = terms.map((t, i) => {
      const rank = i + 1;
      const medals = { 1: '🥇', 2: '🥈', 3: '🥉' };
      return `
      <div class="flex items-center gap-3 p-3 rounded-lg hover:bg-base-300 transition-colors border-b border-base-300/50 last:border-0">
        <span class="text-lg font-bold text-base-content/20 w-7 text-right">${medals[rank] || `#${rank}`}</span>
        <div class="avatar placeholder">
          <div class="w-8 rounded-full bg-base-300 text-xs">${medals[rank] ? medals[rank] : '🔍'}</div>
        </div>
        <div class="flex-1 min-w-0">
          <div class="font-medium text-sm truncate">${t.title}</div>
          <div class="flex gap-2 items-center mt-0.5">
            <span class="badge badge-ghost badge-xs">${t.source}</span>
            <span class="text-[10px] text-base-content/40">${Format.timeAgo(t.fetchedAt)}</span>
          </div>
        </div>
        <div class="radial-progress text-success text-xs" style="--value:${Math.max(10, 100 - i * 8)};--size:2rem;--thickness:3px">${100 - i * 8}%</div>
      </div>`;
    }).join('');
  } catch {
    container.innerHTML = `
      <div class="flex flex-col items-center py-12 text-base-content/50">
        <span class="text-4xl mb-3">📭</span>
        <p class="text-sm mb-1">Trending data unavailable</p>
        <p class="text-xs">Google Trends RSS may be blocked in your region</p>
      </div>`;
  }
};
