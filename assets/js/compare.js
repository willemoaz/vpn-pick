/* ==========================================================================
   compare.js — progressive enhancement for the comparison table.
   The table is rendered server-side as a real <table> for accessibility and
   search engines; this script only adds filtering and sorting on top.
   With JS disabled the full unfiltered table remains readable, and every
   filter also lives in the URL so a filtered view can be shared.
   ========================================================================== */
(function () {
  'use strict';

  var table = document.getElementById('cmp-table');
  if (!table) return;

  var tbody   = table.querySelector('tbody');
  var rows    = Array.prototype.slice.call(tbody.querySelectorAll('tr'));
  var cards   = Array.prototype.slice.call(document.querySelectorAll('.cmp-card'));
  var items   = rows.concat(cards);
  var search  = document.getElementById('cmp-search');
  var sortSel = document.getElementById('cmp-sort');
  var useSel  = document.getElementById('cmp-usecase');
  var freeSel = document.getElementById('cmp-free');
  var empty   = document.getElementById('cmp-empty');
  var status  = document.getElementById('cmp-status');
  var reset   = document.getElementById('cmp-reset');
  var share   = document.getElementById('cmp-share');
  var tableWrap = table.closest('.table-wrap');

  var headers = Array.prototype.slice.call(table.querySelectorAll('thead th.sortable'));
  var params  = new URLSearchParams(window.location.search);

  /* ------------------------------------------------------------- utilities */
  function cellVal(tr, key) {
    var td = tr.querySelector('td[data-key="' + key + '"]');
    if (td) {
      var n = parseFloat(td.getAttribute('data-sort'));
      if (!isNaN(n)) return n;
    }
    // Fall back to a row-level data attribute (used by data-servers, data-rank)
    var attr = parseFloat(tr.getAttribute('data-' + key));
    return isNaN(attr) ? 0 : attr;
  }

  function matchesFilters(el) {
    var q = (search && search.value || '').trim().toLowerCase();
    if (q) {
      var hay = (el.getAttribute('data-name') || '').toLowerCase();
      var head = (el.getAttribute('data-headquarters') || '').toLowerCase();
      if (hay.indexOf(q) === -1 && head.indexOf(q) === -1) return false;
    }
    if (useSel && useSel.value) {
      var cases = (el.getAttribute('data-cases') || '').split(' ');
      if (cases.indexOf(useSel.value) === -1) return false;
    }
    if (freeSel && freeSel.value === 'yes' && el.getAttribute('data-free') !== 'yes') return false;
    if (freeSel && freeSel.value === 'unlimited' && el.getAttribute('data-unlimited') !== 'yes') return false;
    if (freeSel && freeSel.value === 'open-source' && el.getAttribute('data-opensource') !== 'yes') return false;
    if (freeSel && freeSel.value === 'anonymous' && el.getAttribute('data-anonymous') !== 'yes') return false;
    return true;
  }

  /* ------------------------------------------------------- URL as state */
  function writeUrl() {
    if (!window.history || !window.history.replaceState) return;
    var q = new URLSearchParams(window.location.search);
    function set(key, value) { if (value) q.set(key, value); else q.delete(key); }
    set('q', search && search.value.trim());
    set('use', useSel && useSel.value);
    set('free', freeSel && freeSel.value);
    var sort = sortSel && sortSel.value;
    if (sort && sort !== 'score:desc') set('sort', sort); else q.delete('sort');
    var s = q.toString();
    try {
      history.replaceState(null, '', window.location.pathname + (s ? '?' + s : '') + window.location.hash);
    } catch (e) {}
  }

  function readUrl() {
    if (search && params.get('q')) search.value = params.get('q');
    if (useSel && params.get('use')) useSel.value = params.get('use');
    if (freeSel && params.get('free')) freeSel.value = params.get('free');
    return params.get('sort');
  }

  /* ------------------------------------------------------------- apply all */
  function apply() {
    var shownRows = 0;
    var shownCards = 0;
    rows.forEach(function (tr) {
      var ok = matchesFilters(tr);
      tr.hidden = !ok;
      if (ok) shownRows++;
    });
    // The card view replaces the table under 860px, so it needs its own pass
    // or filtering silently stops working on phones.
    cards.forEach(function (card) {
      var ok = matchesFilters(card);
      card.hidden = !ok;
      if (ok) shownCards++;
    });

    var shown = rows.length ? shownRows : shownCards;

    if (status) {
      var all  = status.getAttribute('data-showing-all') || '';
      var some = status.getAttribute('data-showing') || '';
      status.textContent = (shown === rows.length ? all : some)
        .replace(/\{(\w+)\}/g, function (_, key) {
          return { a: String(shown), b: String(rows.length), n: String(rows.length) }[key] || '';
        });
    }
    if (empty) empty.hidden = shown !== 0;
    if (tableWrap) tableWrap.hidden = shown === 0;
    writeUrl();
  }

  /* ------------------------------------------------------------------ sort */
  function sortBy(key, dir) {
    var sorted = rows.slice().sort(function (a, b) {
      var av = cellVal(a, key);
      var bv = cellVal(b, key);
      if (av === bv) {
        return parseInt(a.getAttribute('data-rank'), 10) - parseInt(b.getAttribute('data-rank'), 10);
      }
      return dir === 'asc' ? av - bv : bv - av;
    });
    sorted.forEach(function (tr) { tbody.appendChild(tr); });

    // Mirror the same order in the mobile card list
    var byKey = {};
    cards.forEach(function (c) { byKey[c.getAttribute('data-key')] = c; });
    sorted.forEach(function (tr) {
      var card = byKey[tr.getAttribute('data-key')];
      if (card) card.parentNode.appendChild(card);
    });

    headers.forEach(function (th) {
      if (th.getAttribute('data-key') === key) {
        th.setAttribute('aria-sort', dir === 'asc' ? 'ascending' : 'descending');
      } else {
        th.removeAttribute('aria-sort');
      }
    });

    if (sortSel) {
      var want = key + ':' + dir;
      var has = Array.prototype.some.call(sortSel.options, function (o) {
        return o.value === want;
      });
      if (has) sortSel.value = want;
    }
    try {
      sessionStorage.setItem('vpnpick:cmp-sort', key + ':' + dir);
    } catch (e) {}
    writeUrl();
  }

  headers.forEach(function (th) {
    th.setAttribute('tabindex', '0');
    th.setAttribute('role', 'columnheader');

    /* First-click direction per column: the useful end of the range comes
       first (cheapest price, most devices, free tier present, rank #1,
       privacy-friendly jurisdiction); everything else starts high-to-low. */
    var DEFAULT_DIR = {
      price_month: 'asc',
      rank: 'asc',
      jurisdiction: 'asc',
      free: 'desc'
    };

    function go() {
      var key = th.getAttribute('data-key');
      var current = th.getAttribute('aria-sort');
      var dir = current === 'ascending' ? 'desc'
              : current === 'descending' ? 'asc'
              : (DEFAULT_DIR[key] || 'desc');
      sortBy(key, dir);
    }

    th.addEventListener('click', go);
    th.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(); }
    });
  });

  /* --------------------------------------------------------- dropdown sort */
  function initSort(urlSort) {
    if (!sortSel) return;
    sortSel.addEventListener('change', function () {
      var parts = sortSel.value.split(':');
      sortBy(parts[0], parts[1]);
    });
    if (urlSort && urlSort.indexOf(':') > 0) {
      var p = urlSort.split(':');
      sortBy(p[0], p[1]);
      return;
    }
    var saved;
    try { saved = sessionStorage.getItem('vpnpick:cmp-sort'); } catch (e) {}
    if (saved && saved.indexOf(':') > 0 && sortSelHas(saved)) {
      var s = saved.split(':');
      sortBy(s[0], s[1]);
    } else {
      sortBy('score', 'desc');
    }
  }

  function sortSelHas(value) {
    if (!sortSel) return false;
    return Array.prototype.some.call(sortSel.options, function (o) {
      return o.value === value;
    });
  }

  /* ------------------------------------------------------------- listeners */
  if (search) search.addEventListener('input', apply);
  if (useSel)  useSel.addEventListener('change', apply);
  if (freeSel) freeSel.addEventListener('change', apply);

  if (reset) {
    reset.addEventListener('click', function () {
      if (search) search.value = '';
      if (useSel) useSel.value = '';
      if (freeSel) freeSel.value = '';
      if (sortSel) sortSel.value = 'score:desc';
      sortBy('score', 'desc');
      apply();
      if (search) search.focus();
    });
  }

  if (share) {
    share.addEventListener('click', function () {
      var url = window.location.href;
      var done = function () {
        var msg = share.getAttribute('data-copied') || 'Copied';
        if (window.vpnToast) window.vpnToast(msg);
        share.classList.add('is-done');
        setTimeout(function () { share.classList.remove('is-done'); }, 1800);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(done, function () { window.prompt('', url); });
      } else {
        window.prompt('', url);
      }
    });
  }

  /* ------------------------------------- "start from what you need" tiles */
  document.querySelectorAll('[data-use-pick]').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      if (!useSel) return;                 // controls live on another page: follow the link
      e.preventDefault();
      useSel.value = btn.getAttribute('data-use-pick');
      apply();
      var target = document.getElementById('compare-table')
                || document.getElementById('compare-preview')
                || document.getElementById('compare');
      if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        if (search) { search.focus({ preventScroll: true }); }
      }
    });
  });

  var urlSort = readUrl();
  initSort(urlSort);
  apply();
})();
