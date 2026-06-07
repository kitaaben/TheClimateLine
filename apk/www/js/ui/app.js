const Router = {};

Router.routes = {
  dashboard: { view: Dashboard, label: 'Dashboard' },
  feed: { view: Feed, label: 'Feed' },
  map: { view: MapView, label: 'Map' },
  trending: { view: Trending, label: 'Trending' },
  safety: { view: Safety, label: 'Safety' },
};

Router.current = null;

Router.init = function () {
  const navBtns = document.querySelectorAll('.nav-btn');
  navBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const route = btn.dataset.route;
      window.location.hash = `#/${route}`;
    });
  });

  window.addEventListener('hashchange', () => this.handleRoute());
  if (!window.location.hash || window.location.hash === '#') {
    window.location.hash = '#/dashboard';
  } else {
    this.handleRoute();
  }
};

Router.handleRoute = function () {
  const hash = window.location.hash.replace('#/', '') || 'dashboard';
  const route = hash.split('?')[0];

  if (this.current === route) return;
  this.current = route;

  const view = this.routes[route];
  if (!view) {
    window.location.hash = '#/dashboard';
    return;
  }

  document.querySelectorAll('.nav-btn').forEach(b => {
    b.classList.toggle('nav-active', b.dataset.route === route);
    b.classList.toggle('text-success', b.dataset.route === route);
  });

  if (view.view.render) view.view.render();
};

Router.navigate = function (route) {
  window.location.hash = `#/${route}`;
};

document.addEventListener('DOMContentLoaded', () => {
  Router.init();
});
