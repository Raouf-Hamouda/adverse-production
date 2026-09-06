/* ADVERSE · app.js
   Lenis smooth scroll (Anduril) + GSAP ScrollTrigger reveals (Palantir / Anduril register)
   + digit roller for stats (Anduril) + nav follows the section theme under it + grid-lines toggle (Applied Intuition). */
(() => {
  const root = document.documentElement;
  root.classList.remove('no-js');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- smooth scroll */
  let lenis = null;
  if (window.Lenis && !reduce) {
    lenis = new Lenis({ lerp: 0.1, smoothWheel: true });
    if (window.gsap) { gsap.ticker.add(t => lenis.raf(t * 1000)); gsap.ticker.lagSmoothing(0); }
    else { const raf = t => { lenis.raf(t); requestAnimationFrame(raf); }; requestAnimationFrame(raf); }
  }

  /* ---- reveals: <el data-reveal> or data-reveal="0.2" (delay in s) */
  const reveals = [...document.querySelectorAll('[data-reveal]')];
  if (window.gsap && window.ScrollTrigger && !reduce) {
    gsap.registerPlugin(ScrollTrigger);
    if (lenis) lenis.on('scroll', ScrollTrigger.update);
    reveals.forEach(el => gsap.to(el, { opacity: 1, y: 0, duration: 0.9, delay: parseFloat(el.dataset.reveal) || 0, ease: 'power3.out',
                                        scrollTrigger: { trigger: el, start: 'top 88%', once: true } }));
  } else reveals.forEach(el => { el.style.opacity = 1; el.style.transform = 'none'; });

  /* ---- digit roller: <span data-roll="7" data-pad="2">0</span> */
  const roll = el => {
    const target = parseFloat(el.dataset.roll), pad = parseInt(el.dataset.pad || '0', 10), dur = reduce ? 0 : 1500, t0 = performance.now();
    const fmt = v => { const n = Number.isInteger(target) ? Math.round(v) : v.toFixed(1); return String(n).padStart(pad, '0'); };
    const step = now => { const p = dur ? Math.min(1, (now - t0) / dur) : 1, e = 1 - Math.pow(1 - p, 3); el.textContent = fmt(target * e); if (p < 1) requestAnimationFrame(step); };
    requestAnimationFrame(step);
  };
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { roll(e.target); io.unobserve(e.target); } }), { threshold: 0.5 });
  document.querySelectorAll('[data-roll]').forEach(el => io.observe(el));

  /* ---- nav takes the theme of the section under it */
  const nav = document.querySelector('[data-nav]');
  if (nav) {
    const sections = [...document.querySelectorAll('section[data-theme]')];
    const update = () => { const y = nav.offsetHeight / 2; const s = sections.find(sec => { const r = sec.getBoundingClientRect(); return r.top <= y && r.bottom > y; }); if (s) nav.dataset.on = s.dataset.theme; };
    const hero = document.querySelector('.hero, .mission-hero');
    const solid = () => nav.classList.toggle('scrolled', scrollY > (hero ? hero.offsetHeight - nav.offsetHeight : 24));
    addEventListener('scroll', () => { update(); solid(); }, { passive: true }); update(); solid();
  }

  /* ---- grid lines overlay: press G */
  const lines = document.querySelector('.grid-lines');
  if (lines) {
    const build = () => { const n = parseInt(getComputedStyle(root).getPropertyValue('--cols'), 10) || 12; lines.innerHTML = '<i></i>'.repeat(n); };
    build(); addEventListener('resize', build);
    addEventListener('keydown', e => { if (e.key.toLowerCase() === 'g' && !e.metaKey && !e.ctrlKey && document.activeElement.tagName !== 'INPUT') lines.classList.toggle('on'); });
  }

  window.ADVERSE = { lenis, roll };
})();
