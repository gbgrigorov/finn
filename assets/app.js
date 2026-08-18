/* shared helpers — vanilla, no deps */
const CARS = window.CARS || [];
const eur = n => Math.round(n).toLocaleString('de-DE') + ' €';
const qs  = k => new URLSearchParams(location.search).get(k);
const by  = id => CARS.find(c => c.id === id);
const seg = s => CARS.filter(c => c.seg.includes(s));

/* fake analytics — visible proof the segmentation event fires */
function track(ev, props) {
  const e = { ts: new Date().toISOString(), event: ev, ...props };
  const log = JSON.parse(localStorage.getItem('finn_events') || '[]');
  log.push(e);
  localStorage.setItem('finn_events', JSON.stringify(log.slice(-50)));
  console.log('%c[track]', 'background:#000;color:#fff;padding:2px 6px;border-radius:3px', ev, props || '');
}

const store = {
  get: () => JSON.parse(localStorage.getItem('finn_quiz') || '{}'),
  set: o => localStorage.setItem('finn_quiz', JSON.stringify({ ...store.get(), ...o })),
  clear: () => localStorage.removeItem('finn_quiz')
};

const VARIANT = () => window.VARIANT || 'B';
const HOME = () => VARIANT() === 'C' ? 'index-c.html' : 'index.html';

function header(active) {
  const bold = k => active === k ? 'style="font-weight:600"' : '';
  const links = VARIANT() === 'C'
    ? `<a href="drive.html?type=elektro" ${bold('elektro')}>Elektro</a>
       <a href="drive.html?type=hybrid" ${bold('hybrid')}>Hybrid</a>
       <a href="drive.html?type=verbrenner" ${bold('verbrenner')}>Benzin &amp; Diesel</a>
       <a href="ab-test.html">Der A/B-Test</a>`
    : `<a href="small.html" ${bold('small')}>Klein &amp; günstig</a>
       <a href="family.html" ${bold('family')}>Familie</a>
       <a href="sport.html" ${bold('sport')}>Sport</a>
       <a href="ab-test.html">Der A/B-Test</a>`;
  return `<header class="nav"><div class="nav-in">
    <a href="${HOME()}" class="logo">FINN</a>
    <nav class="nav-links">${links}</nav>
    <div class="nav-icons">
      <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg>
      <svg viewBox="0 0 24 24"><path d="M3 4h2l2.4 11h10.2L20 7H6"/><circle cx="9" cy="19" r="1.4"/><circle cx="17" cy="19" r="1.4"/></svg>
      <svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7"/></svg>
    </div>
  </div></header>`;
}

function footer() {
  return `<footer><div class="wrap">
    <div class="cols">
      <div><div class="logo" style="color:#fff">FINN</div>
        <p style="margin-top:14px;max-width:280px">Das Auto-Abo mit allem drin. Ein Preis, keine Überraschungen.</p></div>
      <div><h4>Variante B — Bedarf</h4><a href="small.html">Klein &amp; günstig</a><a href="family.html">Familienautos</a><a href="sport.html">Sport &amp; Premium</a></div>
      <div><h4>Variante C — Antrieb</h4><a href="drive.html?type=elektro">Elektro</a><a href="drive.html?type=hybrid">Hybrid</a><a href="drive.html?type=verbrenner">Benzin &amp; Diesel</a></div>
      <div><h4>Prototyp</h4><a href="ab-test.html">Testkonzept</a><a href="index.html">Variante B</a><a href="index-c.html">Variante C</a></div>
    </div>
    <div class="fbot">Klickbarer Prototyp — gebaut von Gabe Grigorov als Diskussionsgrundlage. Kein Produkt von FINN. Bilder &amp; Fahrzeugdaten stammen von finn.com und dienen nur der Illustration.</div>
  </div></footer>`;
}

function abBadge() {
  const v = VARIANT();
  const tab = (k, href, label) =>
    `<a href="${href}" class="abx-t ${v === k ? 'on' : ''}" title="${label}">${k}</a>`;
  return `<div class="abx">
    <span class="abx-l">Variante</span>
    ${tab('B', 'index.html', 'Bedarf: Klein · Familie · Sport')}
    ${tab('C', 'index-c.html', 'Antrieb: Elektro · Hybrid · Benzin')}
    <a href="ab-test.html" class="abx-doc">Testkonzept</a>
  </div>`;
}

function carCard(c, opts = {}) {
  const t = opts.tag ? `<span class="tag ${opts.tagClass || ''}">${opts.tag}</span>` : '';
  const specs = opts.specs || `${c.seats} Sitze · ${c.ps} PS · ${c.fuel}`;
  return `<a class="card" href="car.html?id=${encodeURIComponent(c.id)}&from=${opts.from||''}">
    ${t}
    <div class="ph"><img src="${c.img}" alt="${c.brand} ${c.model}" loading="lazy"></div>
    <div class="bd">
      <div class="br">${c.brand}</div>
      <div class="nm">${c.model}</div>
      <div class="sp">${specs}</div>
      <div class="pr"><b>${eur(c.price)}</b><span>/Monat · ${c.term} Mon.</span></div>
    </div></a>`;
}

function mount(active) {
  const h = document.getElementById('hdr'); if (h) h.outerHTML = header(active);
  const f = document.getElementById('ftr'); if (f) f.outerHTML = footer() + abBadge();
}

/* counts, so the copy stays true when the dataset changes */
const drive = t => CARS.filter(c => c.drive_type === t);
const priceFrom = list => eur(Math.min(...list.map(c => c.price)));
