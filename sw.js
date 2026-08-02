// LongTai Jiang 個人網站 Service Worker
const CACHE_NAME = 'longtai-v7';
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/blogs.html',
  '/404.html',
  '/robots.txt',
  '/sitemap.xml',
  '/public/css/bundle.css',
  '/public/css/blogs.css',
  '/public/css/markdown.css',
  '/public/javascript/main.js',
  '/public/javascript/ui.js',
  '/public/javascript/utils.js',
  '/public/javascript/experiences.js',
  '/public/javascript/friends.js',
  '/public/javascript/support.js',
  '/public/javascript/ads.js',
  '/public/javascript/special.js',
  '/public/javascript/blogs.js',
  '/public/javascript/blogs_preview.js',
  '/public/json/experiences.json',
  '/public/json/friends.json',
  '/public/json/support.json',
  '/public/json/ads.json',
  '/public/json/links.json',
  '/public/images/me.webp',
  '/public/images/me.png',
  '/public/images/nopng.webp',
  '/public/manifest.webmanifest',
  '/.well-known/ai-plugin.json'
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

// 攔截請求：靜態資源快取優先，部落格文章網路優先
self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;

  const url = new URL(event.request.url);
  const isDynamicContent = url.pathname.startsWith('/public/blogs/') || url.pathname === '/public/json/blogs.json';

  if (isDynamicContent) {
    // 網路優先 (Network First) 策略：針對經常變動的部落格內容
    event.respondWith(
      fetch(event.request)
        .then(response => {
          if (response && response.status === 200) {
            const responseToCache = response.clone();
            caches.open(CACHE_NAME).then(cache => cache.put(event.request, responseToCache));
          }
          return response;
        })
        .catch(() => {
          return caches.match(event.request);
        })
    );
  } else {
    // 快取優先 (Cache First) 策略：針對靜態資源
    event.respondWith(
      caches.match(event.request)
        .then(cached => {
          if (cached) return cached;
          return fetch(event.request)
            .then(response => {
              if (!response || response.status !== 200 || !response.url.startsWith(self.location.origin)) {
                return response;
              }
              const responseToCache = response.clone();
              caches.open(CACHE_NAME).then(cache => cache.put(event.request, responseToCache));
              return response;
            })
            .catch(() => {
              if (event.request.mode === 'navigate') {
                return caches.match('/index.html');
              }
            });
        })
    );
  }
});