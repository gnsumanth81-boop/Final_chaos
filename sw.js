// ═══════════════════════════════════════════════════════
// CHAOS INTELLIGENCE — SERVICE WORKER v1
// Cache-first for shell assets, network-first for live data
// ═══════════════════════════════════════════════════════

const CACHE_NAME = 'chaos-terminal-v17';

// Shell assets cached on install — the UI loads instantly offline
const SHELL_ASSETS = [
  '/',
  '/index.html',
  '/icon.svg',
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
// Network-first for live JSON data (latest.json, signals.json)
// Cache-first for everything else (HTML, CSS, fonts, icons)
self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);

  // Skip non-GET requests and cross-origin requests
  if (event.request.method !== 'GET' || url.origin !== location.origin) return;

  // Live data endpoints — always try network first
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          // Clone and cache the fresh response
          const clone = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
          return response;
        })
        .catch(() => caches.match(event.request)) // Offline fallback to cached data
    );
    return;
  }

  // Shell assets — cache-first for instant load
  event.respondWith(
    caches.match(event.request)
      .then((cached) => {
        if (cached) return cached;
        return fetch(event.request).then((response) => {
          // Cache new assets dynamically (fonts, etc.)
          if (response.ok) {
            const clone = response.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
          }
          return response;
        });
      })
  );
});
