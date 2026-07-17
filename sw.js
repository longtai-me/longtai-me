// LongTai Jiang 個人網站 Service Worker
const CACHE_NAME = 'longtai-v1';
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/404.html',
  '/public/css/bundle.css',
  '/public/javascript/main.js',
  '/public/javascript/ui.js',
  '/public/javascript/utils.js',
  '/public/javascript/experiences.js',
  '/public/javascript/friends.js',
  '/public/javascript/support.js',
  '/public/javascript/ads.js',
  '/public/javascript/special.js',
  '/public/json/experiences.json',
  '/public/json/friends.json',
  '/public/json/support.json',
  '/public/json/ads.json',
  '/public/json/links.json',
  '/public/images/me.webp',
  '/public/images/nopng.webp'
];

// 安裝：預快取靜態資源
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(STATIC_ASSETS))
      .then(() => self.skipWaiting())
  );
});

// 啟用：清除舊快取
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(
        keys.filter(key => key !== CACHE_NAME)
          .map(key => caches.delete(key))
      ))
      .then(() => self.clients.claim())
  );
});

// 攔截請求：快取優先，網路 fallback
self.addEventListener('fetch', event => {
  // 只處理 GET 請求
  if (event.request.method !== 'GET') return;

  event.respondWith(
    caches.match(event.request)
      .then(cached => {
        // 快取命中則回傳
        if (cached) return cached;

        // 否則從網路取得，並快取成功的回應
        return fetch(event.request)
          .then(response => {
            // 只快取同源且成功的回應
            if (!response || response.status !== 200 || !response.url.startsWith(self.location.origin)) {
              return response;
            }
            const responseToCache = response.clone();
            caches.open(CACHE_NAME)
              .then(cache => cache.put(event.request, responseToCache));
            return response;
          })
          .catch(() => {
            // 網路失敗時，若為導航請求則回傳首頁
            if (event.request.mode === 'navigate') {
              return caches.match('/index.html');
            }
          });
      })
  );
});