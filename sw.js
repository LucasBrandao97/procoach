// ProCoach Football · guarda o jogo para uso offline.
// Estratégia: com internet, sempre busca a versão nova (e guarda uma cópia); sem internet, usa a cópia guardada.
const CACHE = 'procoach-v1';
const BASE = ['./', 'index.html', 'manifest.webmanifest', 'icon-192.png', 'icon-512.png', 'icon-maskable-512.png', 'apple-touch-icon.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(BASE)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  const fonte = url.hostname === 'fonts.googleapis.com' || url.hostname === 'fonts.gstatic.com';
  if (url.origin !== self.location.origin && !fonte) return;

  if (fonte) {
    // fontes: usa a guardada e atualiza em segundo plano
    e.respondWith(caches.open(CACHE).then(c => c.match(req).then(hit => {
      const rede = fetch(req).then(r => { c.put(req, r.clone()); return r; }).catch(() => hit);
      return hit || rede;
    })));
    return;
  }
  // jogo e arquivos do site: rede primeiro, cópia guardada se estiver sem sinal
  e.respondWith(
    fetch(req).then(r => {
      if (r && r.ok) { const cp = r.clone(); caches.open(CACHE).then(c => c.put(req, cp)); }
      return r;
    }).catch(() => caches.match(req).then(hit => hit || (req.mode === 'navigate' ? caches.match('index.html') : undefined)))
  );
});
