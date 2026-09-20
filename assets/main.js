/* All Wrapped Up — site behaviour (no dependencies) */
(function () {
  'use strict';

  // Sticky header shadow
  var header = document.querySelector('.site-header');
  function onScroll() { if (header) header.classList.toggle('scrolled', window.scrollY > 8); }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  // Mobile nav
  var toggle = document.querySelector('.nav-toggle');
  var links = document.querySelector('.nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      var open = links.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && links.classList.contains('open')) { links.classList.remove('open'); toggle.setAttribute('aria-expanded', 'false'); toggle.focus(); }
    });
  }

  // Scroll reveal
  var revealEls = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && revealEls.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    revealEls.forEach(function (el) { io.observe(el); });
  } else { revealEls.forEach(function (el) { el.classList.add('in'); }); }

  // Footer year
  document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });

  // Holiday countdown (days until Dec 25 + suggested booking deadline)
  var cd = document.querySelector('[data-countdown]');
  if (cd) {
    var now = new Date();
    var xmas = new Date(now.getFullYear(), 11, 25);
    if (now > xmas) xmas = new Date(now.getFullYear() + 1, 11, 25);
    var diff = xmas - now;
    var days = Math.floor(diff / 864e5), hrs = Math.floor(diff % 864e5 / 36e5), mins = Math.floor(diff % 36e5 / 6e4);
    cd.innerHTML = '<div><b>' + days + '</b><span>days</span></div><div><b>' + hrs + '</b><span>hours</span></div><div><b>' + mins + '</b><span>minutes</span></div>';
    var slot = document.querySelector('[data-book-by]');
    if (slot) {
      var bookBy = new Date(xmas); bookBy.setDate(bookBy.getDate() - 14);
      slot.textContent = bookBy.toLocaleDateString('en-US', { month: 'long', day: 'numeric' });
    }
  }

  // Price estimator: Classic wrapping is priced by the group, materials included
  function groupPrice(n) { if (n <= 0) return 0; if (n <= 10) return 60; if (n <= 25) return 80; if (n <= 50) return 100; return 120 + (n - 51) * 2.4; }
  var PER_GIFT = { notes: 2, luxe: 4 };
  var OVERSIZED = 15, DELIVERY = 50;
  var DISCOUNTS = { nobows: 15, boxed: 10, reuse: 10 };
  function money(n) { return '$' + Math.round(n).toLocaleString('en-US'); }

  document.querySelectorAll('[data-estimator]').forEach(function (form) {
    var out = form.querySelector('[data-amount]');
    var brk = form.querySelector('[data-breakdown]');
    var save = form.querySelector('[data-save]');
    var link = form.querySelector('[data-quote-link]');
    function num(name) { var el = form.querySelector('[name="' + name + '"]'); return el ? Math.max(0, parseInt(el.value, 10) || 0) : 0; }
    function on(name) { var el = form.querySelector('[name="' + name + '"]'); return !!(el && el.checked); }
    function calc() {
      var total = num('gifts'), over = Math.min(num('oversized'), total);
      var lg = form.querySelector('[data-count="gifts"]'); if (lg) lg.textContent = total;
      var lo = form.querySelector('[data-count="oversized"]'); if (lo) lo.textContent = over;
      var base = groupPrice(total);
      var extras = over * OVERSIZED;
      Object.keys(PER_GIFT).forEach(function (k) { if (on('addon_' + k)) extras += total * PER_GIFT[k]; });
      var disc = 0;
      Object.keys(DISCOUNTS).forEach(function (k) { if (on('disc_' + k)) disc += DISCOUNTS[k]; });
      disc = Math.min(disc, base);
      var delivery = on('delivery') ? DELIVERY : 0;
      var rushFee = on('rush') ? (base + extras - disc) * 0.25 : 0;
      var est = base + extras - disc + delivery + rushFee;
      if (out) out.textContent = total ? money(est) + ' – ' + money(est * 1.15) : '$0';
      if (brk) {
        var parts = [];
        if (total) { var tier = total <= 10 ? 'small group' : total <= 25 ? 'medium group' : total <= 50 ? 'large group' : 'extra large group'; parts.push(total + ' gift' + (total === 1 ? '' : 's') + ' · ' + tier + ' ' + money(base)); }
        if (over) parts.push(over + ' oversized +' + money(over * OVERSIZED));
        if (extras - over * OVERSIZED) parts.push('add-ons +' + money(extras - over * OVERSIZED));
        if (delivery) parts.push('pickup & delivery +' + money(delivery));
        if (rushFee) parts.push('rush +25%');
        brk.textContent = parts.length ? parts.join(' · ') : 'Add a few gifts to see an estimate.';
      }
      if (save) { save.hidden = !disc; if (disc) save.textContent = 'You save ' + money(disc) + ' with discounts'; }
      if (link) link.setAttribute('href', '/contact/?gifts=' + total + '&oversized=' + over + '&estimate=' + encodeURIComponent(out ? out.textContent : ''));
    }
    form.addEventListener('input', calc); form.addEventListener('change', calc); calc();
  });

  // Pre-fill contact form from estimator link
  var contactForm = document.querySelector('form[data-contact]');
  if (contactForm) {
    var p = new URLSearchParams(location.search);
    var gifts = p.get('gifts');
    var msg = contactForm.querySelector('[name="message"]');
    var count = contactForm.querySelector('[name="gift_count"]');
    if (gifts && count && !count.value) count.value = gifts;
    if (gifts && msg && !msg.value) {
      msg.value = 'Estimate from your website: ' + (p.get('estimate') || '') + '\n' +
        'Gifts: ' + (p.get('gifts') || 0) + ', Oversized: ' + (p.get('oversized') || 0) + '\n\n';
    }
    var type = p.get('type'); var sel = contactForm.querySelector('[name="client_type"]');
    if (type && sel) sel.value = type;
    // mailto fallback: builds an email if the form endpoint is unreachable (works offline / before form activation)
    var fallback = contactForm.querySelector('[data-mailto]');
    if (fallback) {
      fallback.addEventListener('click', function (e) {
        e.preventDefault();
        var fd = new FormData(contactForm), lines = [];
        fd.forEach(function (v, k) { if (k.charAt(0) !== '_' && v) lines.push(k.replace(/_/g, ' ') + ': ' + v); });
        location.href = 'mailto:' + (contactForm.getAttribute('data-mailto-to') || '') + '?subject=' + encodeURIComponent('Gift wrapping quote request') + '&body=' + encodeURIComponent(lines.join('\n'));
      });
    }
  }

  // Testimonial rotator (only on small screens where the grid collapses)
  var quotes = document.querySelectorAll('.quotes .quote');
  if (quotes.length > 1 && window.matchMedia('(max-width:560px)').matches && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var i = 0; quotes.forEach(function (q, idx) { q.style.display = idx ? 'none' : ''; });
    setInterval(function () { quotes[i].style.display = 'none'; i = (i + 1) % quotes.length; quotes[i].style.display = ''; }, 6000);
  }
})();
