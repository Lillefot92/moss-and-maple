import json, subprocess, os, sys
sys.path.insert(0, '.')
import pages
meta = pages.build('out')
order = {'spring':0,'summer':1,'autumn':2,'winter':3}
seq = {'spring-blossom':0,'spring-tulips':1,'spring-mandala':2,'summer-sunflowers':0,'summer-butterfly':1,'summer-sun':2,
       'autumn-leaves':0,'autumn-mushrooms':1,'autumn-mandala':2,'winter-cabin':0,'winter-snowflakes':1,'winter-wreath':2}
meta.sort(key=lambda p:(order[p['season']], seq[p['id']]))
app = open('app.html').read().replace('/*PAGES*/[]', json.dumps(meta, separators=(',',':')))
os.makedirs('dist', exist_ok=True)
open('dist/index.html','w').write(app)
icon = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" fill="#f4efe6"/><circle cx="32" cy="33" r="24" fill="#e3eadc"/><path d="M32 50V24" stroke="#5f7454" stroke-width="2.2" stroke-linecap="round" fill="none"/><path d="M32 14l4.5 7.5 7.5-3-2.5 8 7 3.5-7 3 1.5 6-6.5-2.5L32 44l-.5-6.5-6.5 2.5 1.5-6-7-3 7-3.5-2.5-8 7.5 3z" fill="#c47e5a" stroke="#3a312a" stroke-width="1.4" stroke-linejoin="round"/><path d="M32 50c-8 0-13-3-15-7 6-1 11 1 15 7z" fill="#a9bf98" stroke="#3a312a" stroke-width="1.4" stroke-linejoin="round"/></svg>'''
open('dist/icon.svg','w').write(icon)
for size, name in ((512,'icon-512.png'),(192,'icon-192.png'),(180,'apple-touch-icon.png')):
    subprocess.run(['rsvg-convert','-w',str(size),'-h',str(size),'dist/icon.svg','-o','dist/'+name], check=True)
os.remove('dist/icon.svg')
json.dump({"name":"Moss & Maple","short_name":"Moss & Maple","description":"A quiet coloring book of the seasons.",
  "start_url":"./","scope":"./","display":"standalone","orientation":"any","background_color":"#f4efe6","theme_color":"#f4efe6",
  "icons":[{"src":"icon-192.png","sizes":"192x192","type":"image/png"},{"src":"icon-512.png","sizes":"512x512","type":"image/png","purpose":"any maskable"}]},
  open('dist/manifest.webmanifest','w'), indent=2)
open('dist/sw.js','w').write('''// Moss & Maple: keeps the app working offline. Network first, so updates show up right away.
const CACHE = 'moss-maple-v1';
const FILES = ['./', './index.html', './manifest.webmanifest', './icon-192.png', './icon-512.png', './apple-touch-icon.png'];
self.addEventListener('install', e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  e.respondWith(fetch(e.request).then(r => { const copy = r.clone(); caches.open(CACHE).then(c => c.put(e.request, copy)).catch(() => {}); return r; })
    .catch(() => caches.match(e.request).then(r => r || caches.match('./index.html'))));
});
''')
print(os.path.getsize('dist/index.html')//1024, 'KB')
