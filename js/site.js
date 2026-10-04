/* ADVERSE · site.js · page behaviours on top of app.js
   loader (Anduril 1.5 s + roller), mobile menu, marquee, video hover, word reveal + chapter counter (Anduril /space),
   numbered subnav highlight (Palantir), portfolio tabs (Applied), form fallback. */
(() => {
  const root = document.documentElement, reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const A = window.ADVERSE || {};

  /* ---- loader */
  const loader = document.querySelector('.loader');
  if (loader) {
    const pct = loader.querySelector('[data-pct]'); const t0 = performance.now(), dur = reduce ? 0 : 1700;
    if (A.lenis) A.lenis.stop();
    const tick = now => { const p = dur ? Math.min(1, (now - t0) / dur) : 1; if (pct) pct.textContent = String(Math.round(p * 100)).padStart(3, '0'); if (p < 1) requestAnimationFrame(tick); else finish(); };
    const finish = () => { loader.classList.add('done'); if (A.lenis) A.lenis.start(); setTimeout(() => loader.remove(), 700); };
    requestAnimationFrame(tick);
  }

  /* ---- mobile menu */
  const burger = document.querySelector('.burger'), menu = document.querySelector('.menu');
  if (burger && menu) burger.addEventListener('click', () => { const open = menu.classList.toggle('open'); burger.textContent = open ? 'Close' : 'Menu'; burger.setAttribute('aria-expanded', open); root.classList.toggle('menu-open', open); if (A.lenis) open ? A.lenis.stop() : A.lenis.start(); });

  /* ---- marquee: duplicate the track once so it loops seamlessly */
  document.querySelectorAll('.marquee .track').forEach(t => { t.innerHTML += t.innerHTML; });

  /* ---- videos: play on hover (fine pointer) or when in view (touch) */
  const fine = matchMedia('(hover: hover) and (pointer: fine)').matches;
  document.querySelectorAll('video[data-hover]').forEach(v => {
    v.muted = true; v.loop = true; v.playsInline = true;
    const host = v.closest('a, .prow, .project') || v;
    if (fine) { host.addEventListener('mouseenter', () => v.play().catch(() => {})); host.addEventListener('mouseleave', () => v.pause()); }
    else { new IntersectionObserver(es => es.forEach(e => e.isIntersecting ? v.play().catch(() => {}) : v.pause()), { threshold: .5 }).observe(v); }
  });
  document.querySelectorAll('video[autoplay]').forEach(v => { v.muted = true; v.play().catch(() => {}); });

  /* ---- word reveal, scrubbed by scroll */
  const revealWords = el => { el.querySelectorAll('.w').forEach((w, i) => { w.classList.remove('on'); w.style.transitionDelay = (i * 35) + 'ms'; }); requestAnimationFrame(() => requestAnimationFrame(() => el.querySelectorAll('.w').forEach(w => w.classList.add('on')))); };
  document.querySelectorAll('.words').forEach(el => {
    const words = el.textContent.trim().split(/\s+/); el.innerHTML = words.map(w => `<span class="w">${w}</span>`).join(' ');
    const spans = el.querySelectorAll('.w');
    if (el.hasAttribute('data-stagger')) { if (!el.closest('[hidden]')) setTimeout(() => revealWords(el), 300); return; }
    if (window.gsap && window.ScrollTrigger && !reduce) {
      ScrollTrigger.create({ trigger: el, start: 'top 85%', end: 'bottom 45%', scrub: true, onUpdate: s => { const n = Math.round(s.progress * spans.length); spans.forEach((w, i) => w.classList.toggle('on', i < n)); } });
    } else spans.forEach(w => w.classList.add('on'));
  });

  /* ---- capabilities tabs (Anduril /space) */
  document.querySelectorAll('.captabs').forEach(tabs => {
    const buttons = [...tabs.querySelectorAll('.captab')];
    const show = b => {
      buttons.forEach(x => x.setAttribute('aria-selected', x === b));
      document.querySelectorAll('.cappanel').forEach(pn => { const on = pn.id === b.getAttribute('aria-controls'); pn.hidden = !on;
        if (on) { const w = pn.querySelector('.words'); if (w) revealWords(w); const v = pn.querySelector('video'); if (v) v.play().catch(() => {}); } });
      if (window.ScrollTrigger) ScrollTrigger.refresh();
    };
    buttons.forEach(b => b.addEventListener('click', () => show(b)));
    tabs.addEventListener('keydown', e => { const i = buttons.findIndex(b => b.getAttribute('aria-selected') === 'true'); if (e.key === 'ArrowRight') show(buttons[(i + 1) % buttons.length]); if (e.key === 'ArrowLeft') show(buttons[(i - 1 + buttons.length) % buttons.length]); });
    const first = document.querySelector('.cappanel:not([hidden]) video'); if (first) first.play().catch(() => {});
  });

  /* ---- chapter counter 01 / 04 */
  const counter = document.querySelector('.chap-counter');
  if (counter) {
    const chapters = [...document.querySelectorAll('.chapter')], cur = counter.querySelector('[data-cur]'), name = counter.querySelector('[data-name]'), bar = counter.querySelector('.bar i');
    const set = i => { cur.textContent = String(i + 1).padStart(2, '0'); if (name) name.textContent = chapters[i].dataset.title || ''; if (bar) bar.style.width = ((i + 1) / chapters.length * 100) + '%'; };
    if (window.ScrollTrigger) chapters.forEach((c, i) => ScrollTrigger.create({ trigger: c, start: 'top 50%', end: 'bottom 50%', onEnter: () => set(i), onEnterBack: () => set(i) }));
    else new IntersectionObserver(es => es.forEach(e => e.isIntersecting && set(chapters.indexOf(e.target))), { threshold: .5 }).observe && chapters.forEach(c => new IntersectionObserver(es => es.forEach(e => e.isIntersecting && set(chapters.indexOf(e.target))), { threshold: .5 }).observe(c));
    set(0);
    const themed = [...document.querySelectorAll('section[data-theme], footer[data-theme]')];
    const follow = () => { const r = counter.getBoundingClientRect(), y = r.top + r.height / 2; const s = themed.find(sec => { const b = sec.getBoundingClientRect(); return b.top <= y && b.bottom > y; }); if (s && s.dataset.theme !== counter.dataset.theme) counter.dataset.theme = s.dataset.theme; };
    addEventListener('scroll', follow, { passive: true }); follow();
  }

  /* ---- numbered subnav highlight */
  const sub = document.querySelector('.subnav');
  if (sub) {
    const links = [...sub.querySelectorAll('a[href^="#"]')], secs = links.map(a => document.querySelector(a.getAttribute('href'))).filter(Boolean);
    const mark = () => { const y = innerHeight * .35; let on = null; secs.forEach(s => { if (s.getBoundingClientRect().top <= y) on = s; }); links.forEach(a => a.classList.toggle('on', on && a.getAttribute('href') === '#' + on.id)); };
    addEventListener('scroll', mark, { passive: true }); mark();
    links.forEach(a => a.addEventListener('click', e => { const t = document.querySelector(a.getAttribute('href')); if (!t) return; e.preventDefault(); if (A.lenis) A.lenis.scrollTo(t, { offset: -40 }); else t.scrollIntoView({ behavior: 'smooth' }); }));
  }

  /* ---- portfolio tabs */
  const tabs = document.querySelector('.tabs');
  if (tabs) {
    const items = [...document.querySelectorAll('[data-tags]')];
    tabs.addEventListener('click', e => { const b = e.target.closest('.tab'); if (!b) return; const f = b.dataset.filter;
      tabs.querySelectorAll('.tab').forEach(t => t.setAttribute('aria-selected', t === b)); items.forEach(it => it.classList.toggle('hidden', f !== 'all' && !it.dataset.tags.split('|').includes(f)));
      document.querySelectorAll('#films').forEach(sec => { sec.hidden = !sec.querySelector('[data-tags]:not(.hidden)'); });   // no empty Films heading
      if (window.ScrollTrigger) ScrollTrigger.refresh(); });
  }

  /* ---- form: posts JSON to data-endpoint (brand.form_endpoint in site.json); without one, falls back to a prefilled email */
  document.querySelectorAll('form[data-mailto]').forEach(f => f.addEventListener('submit', async e => {
    e.preventDefault(); const d = new FormData(f); if (d.get('website')) return;
    const n = f.querySelector('.note'), say = (t, state) => { if (n) { n.textContent = t; n.dataset.state = state || ''; } }, mail = f.dataset.mailto;
    if (!f.dataset.endpoint) {
      const body = ['Name: ' + d.get('name'), 'Email: ' + d.get('email'), 'Company: ' + (d.get('company') || ''), '', d.get('message')].join('\n');
      location.href = `mailto:${mail}?subject=${encodeURIComponent('Contact from adverseprod.com')}&body=${encodeURIComponent(body)}`; say('Opening your email app'); return;
    }
    d.delete('website'); f.setAttribute('aria-busy', 'true'); say('Sending');
    try {
      const r = await fetch(f.dataset.endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify({ ...Object.fromEntries(d), _subject: 'Contact from adverseprod.com' }) });
      if (!r.ok) throw new Error(r.status);
      f.reset(); say('Message sent. Thank you.', 'ok');
    } catch (err) { say('Could not send. Write to ' + mail, 'error'); }
    f.removeAttribute('aria-busy');
  }));

  /* ---- cursor reticle on the heroes (mouse only): crosshair + frame + position in the frame */
  if (matchMedia('(hover: hover) and (pointer: fine)').matches && !reduce) document.querySelectorAll('.hero, .mission-hero').forEach(hero => {
    const r = document.createElement('div'); r.className = 'reticle'; r.setAttribute('aria-hidden', 'true');
    r.innerHTML = '<i class="h"></i><i class="v"></i><span class="box"></span><span class="xy"></span>'; hero.appendChild(r);
    const [h, v, box, xy] = r.children; let x = 0, y = 0, raf = 0;
    const draw = () => { raf = 0; h.style.transform = `translateY(${y}px)`; v.style.transform = `translateX(${x}px)`; box.style.transform = xy.style.transform = `translate(${x}px, ${y}px)`;
      xy.textContent = 'X ' + String(Math.round(x)).padStart(4, '0') + ' · Y ' + String(Math.round(y)).padStart(4, '0'); };
    hero.addEventListener('mousemove', e => { const b = hero.getBoundingClientRect(); x = e.clientX - b.left; y = e.clientY - b.top; r.classList.add('on'); if (!raf) raf = requestAnimationFrame(draw); });
    hero.addEventListener('mouseleave', () => r.classList.remove('on'));
  });

  /* ---- nav blend: menu open keeps nav readable */
  const nav = document.querySelector('.nav'); if (nav && menu) new MutationObserver(() => nav.style.mixBlendMode = menu.classList.contains('open') ? 'normal' : '').observe(menu, { attributes: true });
})();
