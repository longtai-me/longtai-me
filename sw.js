// Service Worker Uninstaller & Cache Purger
// 清除所有舊快取並自動取消註冊，確保所有使用者每次造訪皆讀取最新內容
self.addEventListener('install', () => {
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.map(key => caches.delete(key))))
      .then(() => self.registration.unregister())
      .then(() => self.clients.claim())
  );
});