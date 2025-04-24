const CACHE_NAME = 'mandarin-cache-v2';  // Change this to force update cache
const ASSETS = [
  '/',                                  // Root page
  '/offline/',                          
  '/static/css/style.css',              
  '/static/js/script.js',               
  '/static/icons/roc.png',              
  '/static/manifest/manifest.json'      
];

// 🔹 Install - Cache Static Assets
self.addEventListener('install', (event) => {
  console.log('Service Worker: Installing...');
  self.skipWaiting();  // Activate immediately
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('Caching app shell...');
      return cache.addAll(ASSETS);
    })
  );
});

// 🔹 Activate - Clean Old Caches
self.addEventListener('activate', (event) => {
  console.log('Service Worker: Activating...');
  clients.claim(); // Control all clients immediately
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cache) => {
          if (cache !== CACHE_NAME) {
            console.log('Deleting old cache:', cache);
            return caches.delete(cache);
          }
        })
      );
    })
  );
});

// 🔹 Fetch - Handle Network Requests
self.addEventListener('fetch', (event) => {
  const requestUrl = new URL(event.request.url);

  // Handle API requests - don't cache
  if (requestUrl.pathname.startsWith('/api/')) {
    event.respondWith(
      fetch(event.request).catch(() => {
        return new Response(JSON.stringify({ error: 'Offline' }), {
          headers: { 'Content-Type': 'application/json' }
        });
      })
    );
    return;
  }

  // Static requests - cache first, then fallback to network
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request).catch(() => {
        if (event.request.headers.get('accept').includes('text/html')) {
          return caches.match('/offline/');
        }
      });
    })
  );
});

// 🔹 Allow Frontend to Trigger Skip Waiting
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
