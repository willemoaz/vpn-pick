/* ==========================================================================
   app.js — progressive enhancement only.
   Every page works with this file blocked. Nothing here is required to read
   the site; it only adds theme switching, navigation and formatting niceties.
   ========================================================================== */
(function () {
  'use strict';

  var LS = {
    theme: 'vpnpick:theme',
    consent: 'vpnpick:consent'
  };

  var html = document.documentElement;

  /* ---------------------------------------------------------------- theme */
  function getTheme() {
    try { return localStorage.getItem(LS.theme); } catch (e) { return null; }
  }
  function setTheme(t) {
    html.setAttribute('data-theme', t);
    try { localStorage.setItem(LS.theme, t); } catch (e) {}
    var btn = document.querySelector('[data-theme-toggle]');
    if (btn) btn.setAttribute('aria-label', t === 'light' ? 'Switch to dark theme' : 'Switch to light theme');
  }
  (function initTheme() {
    var saved = getTheme();
    if (saved === 'light' || saved === 'dark') { setTheme(saved); }
  })();

  document.addEventListener('click', function (e) {
    var t = e.target.closest('[data-theme-toggle]');
    if (!t) return;
    setTheme(html.getAttribute('data-theme') === 'light' ? 'dark' : 'light');
  });

  /* ------------------------------------------------------------- mobile nav */
  var navToggle = document.querySelector('[data-nav-toggle]');
  var nav = document.getElementById('site-nav');
  if (navToggle && nav) {
    navToggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      navToggle.setAttribute('aria-expanded', String(open));
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        nav.classList.remove('is-open');
        navToggle.setAttribute('aria-expanded', 'false');
      }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) {
        nav.classList.remove('is-open');
        navToggle.setAttribute('aria-expanded', 'false');
        navToggle.focus();
      }
    });
  }

  /* ------------------------------------------------------------------ toast */
  var toastTimer;
  window.vpnToast = function (msg) {
    var t = document.getElementById('vpn-toast');
    if (!t) {
      t = document.createElement('div');
      t.id = 'vpn-toast';
      t.className = 'toast';
      t.setAttribute('role', 'status');
      t.setAttribute('aria-live', 'polite');
      document.body.appendChild(t);
    }
    t.textContent = msg;
    // force reflow so the transition runs on repeat calls
    void t.offsetWidth;
    t.classList.add('is-open');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { t.classList.remove('is-open'); }, 3200);
  };

  /* ---------------------------------------------------------------- consent */
  var banner = document.getElementById('consent-banner');
  function readConsent() {
    try { return localStorage.getItem(LS.consent); } catch (e) { return null; }
  }
  // Google Consent Mode: analytics storage stays denied (the inline default)
  // unless the visitor accepted in our banner. The inline gtag() stub always
  // exists, so this is safe even when the tag script itself is blocked.
  function applyAnalyticsConsent() {
    if (typeof window.gtag !== 'function') return;
    var granted = false;
    try { granted = localStorage.getItem(LS.consent) === 'accepted'; } catch (e) {}
    window.gtag('consent', 'update', {
      'analytics_storage': granted ? 'granted' : 'denied'
    });
  }
  applyAnalyticsConsent();
  if (banner) {
    if (!readConsent()) {
      // Slight delay so it never fights the page-load layout
      setTimeout(function () { banner.classList.add('is-open'); }, 700);
    }
    banner.addEventListener('click', function (e) {
      var b = e.target.closest('[data-consent]');
      if (!b) return;
      var v = b.getAttribute('data-consent');
      try { localStorage.setItem(LS.consent, v); } catch (err) {}
      banner.classList.remove('is-open');
      applyAnalyticsConsent();
      if (v === 'accepted') {
        window.vpnToast(banner.getAttribute('data-saved') || 'Preferences saved.');
      }
    });
  }

  /* ------------------------------------------------------------ header state */
  var header = document.querySelector('.site-header');
  if (header) {
    var onScroll = function () {
      header.style.boxShadow = window.scrollY > 8 ? 'var(--shadow-md)' : 'none';
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ------------------------------------------------- plan picker (reviews) */
  var picker = document.querySelector('[data-plan-picker]');
  if (picker) {
    var priceEl = document.querySelector('[data-plan-price]');
    var plans = [];
    try { plans = JSON.parse(priceEl.getAttribute('data-plans') || '[]'); } catch (e) {}
    var chips = Array.prototype.slice.call(picker.querySelectorAll('[data-plan]'));
    var rows  = Array.prototype.slice.call(document.querySelectorAll('[data-plan-row]'));

    var selectPlan = function (i) {
      var model = plans[i];
      if (!model || !priceEl) return;
      chips.forEach(function (chip) {
        var on = Number(chip.getAttribute('data-plan')) === i;
        chip.classList.toggle('is-active', on);
        chip.setAttribute('aria-pressed', String(on));
      });
      rows.forEach(function (row) {
        row.classList.toggle('is-active', Number(row.getAttribute('data-plan-row')) === i);
      });
      var now = priceEl.querySelector('.price__now');
      var total = priceEl.querySelector('.price__total');
      if (now) now.textContent = model.monthly;
      if (total) total.textContent = model.line;
      priceEl.setAttribute('data-selected-plan', String(i));
    };

    chips.forEach(function (chip) {
      chip.addEventListener('click', function () {
        selectPlan(Number(chip.getAttribute('data-plan')));
      });
    });
  }

  /* ------------------------------------------------------------ back to top */
  var reduceMotion = window.matchMedia
    && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var toTop = null;
  if (document.getElementById('main')) {
    toTop = document.createElement('button');
    toTop.type = 'button';
    toTop.className = 'to-top';
    toTop.setAttribute('data-back-to-top', '');
    toTop.setAttribute('aria-label', backToTopLabel());
    toTop.innerHTML = upIcon();
    toTop.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' });
      var skip = document.querySelector('.skip-link');
      if (skip) skip.focus({ preventScroll: true });
    });
    document.body.appendChild(toTop);
    var onScrollTop = function () {
      if (toTop) toTop.classList.toggle('is-visible', window.scrollY > 640);
    };
    window.addEventListener('scroll', onScrollTop, { passive: true });
    onScrollTop();
  }

  function backToTopLabel() {
    return html.getAttribute('lang') === 'sv' ? 'Till toppen' : 'Back to top';
  }
  function upIcon() {
    return '<svg aria-hidden="true" focusable="false" width="18" height="18">'
         + '<use href="#i-arrow-up"/></svg>';
  }

  /* --------------------------------------------------------- scroll reveal */
  if (!reduceMotion && 'IntersectionObserver' in window) {
    var targets = document.querySelectorAll(
      '.section-head, .card-grid, .table-wrap, .cmp-cards, .stats, .proscons, .cta-band .wrap'
    );
    var below = [];
    targets.forEach(function (el) {
      // Anything already on screen is shown at once: never hide content that
      // is in the first paint, and never depend on the observer to reveal it.
      if (el.getBoundingClientRect().top > window.innerHeight * 0.92) below.push(el);
    });
    if (below.length) {
      var revealAll = function () {
        below.forEach(function (el) { el.classList.add('is-visible'); });
      };
      below.forEach(function (el) { el.classList.add('reveal'); });
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            io.unobserve(entry.target);
          }
        });
      }, { rootMargin: '0px 0px -6% 0px', threshold: 0.02 });
      below.forEach(function (el) { io.observe(el); });
      // Belt and braces: nothing may stay invisible if the observer never fires.
      setTimeout(revealAll, 2000);
      window.addEventListener('load', function () { setTimeout(revealAll, 1200); });
    }
  }
})();