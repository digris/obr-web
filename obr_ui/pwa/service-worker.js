self.addEventListener("install", (e) => {
  console.log("[Service Worker] install", e);
  self.skipWaiting();
});

self.addEventListener("fetch", (e) => {
  console.log("[Service Worker] fetch", e);
  e.respondWith(fetch(e.request));
});

self.addEventListener("activate", (e) => {
  console.log("[Service Worker] activate", e);
  // eslint-disable-next-line no-undef
  e.waitUntil(clients.claim());
});
