// ═══════════════════════════════════════════════════════
// CHAOS INTELLIGENCE — SERVICE WORKER v1
// Cache-first for shell assets, network-first for live data
// ═══════════════════════════════════════════════════════

const CACHE_NAME = 'chaos-terminal-v31';

// Shell assets cached on install — the UI loads instantly offline
const SHELL_ASSETS = [
  '/',
  '/index.html',
  '/favicon-32x32.png',
  '/favicon-16x16.png',
  '/apple-touch-icon.png',
  '/manifest.json'
];

// ── INSTALL ──
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(SHELL_ASSETS))
      .then(() => self.skipWaiting())
  );
});

// ── ACTIVATE ──
// Purge stale caches from previous versions
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys.filter((key) => key !== CACHE_NAME)
            .map((key) => caches.delete(key))
      )
    ).then(() => self.clients.claim())
  );
});

// ── FETCH STRATEGY ──
// Network-first for live JSON data AND index.html (to ensure code updates propagate)
// Cache-first for static assets only (icons, fonts, manifest)
self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);

  // Skip non-GET requests and cross-origin requests
  if (event.request.method !== 'GET' || url.origin !== location.origin) return;

  // Network-first: API data, index.html, and the root page
  const isLiveAsset = url.pathname.startsWith('/api/') ||
                      url.pathname === '/' ||
                      url.pathname === '/index.html' ||
                      url.pathname === '/sw.js';

  if (isLiveAsset) {
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          const clone = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
          return response;
        })
        .catch(() => caches.match(event.request))
    );
    return;
  }

  // Static assets — cache-first for instant load (icons, fonts, manifest)
  event.respondWith(
    caches.match(event.request)
      .then((cached) => {
        if (cached) return cached;
        return fetch(event.request).then((response) => {
          if (response.ok) {
            const clone = response.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
          }
          return response;
        });
      })
  );
});
