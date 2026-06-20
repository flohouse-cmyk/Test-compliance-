/* PeopleEdge — shared interactions: sticky nav, mobile menu, FAQ, scroll reveal */
(function () {
  // Navbar scroll state
  var navbar = document.querySelector('.navbar');
  if (navbar) {
    window.addEventListener('scroll', function () {
      navbar.classList.toggle('scrolled', window.scrollY > 20);
    }, { passive: true });
  }

  // Mobile menu
  var hamburger = document.getElementById('hamburger');
  var mobileMenu = document.getElementById('mobile-menu');
  if (hamburger && mobileMenu) {
    hamburger.addEventListener('click', function () {
      var isOpen = mobileMenu.classList.toggle('open');
      hamburger.setAttribute('aria-expanded', isOpen);
    });
    mobileMenu.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        mobileMenu.classList.remove('open');
        hamburger.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // FAQ accordion
  document.querySelectorAll('.faq-trigger').forEach(function (trigger) {
    trigger.addEventListener('click', function () {
      var item = trigger.closest('.faq-item');
      var isOpen = item.classList.toggle('open');
      trigger.setAttribute('aria-expanded', isOpen);
    });
  });

  // Scroll reveal (respects reduced motion)
  var prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var revealEls = document.querySelectorAll('[data-reveal], [data-reveal-stagger]');
  if (prefersReduced || !('IntersectionObserver' in window)) {
    revealEls.forEach(function (el) { el.classList.add('is-visible'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        if (el.hasAttribute('data-reveal-stagger')) {
          Array.prototype.slice.call(el.children).forEach(function (child, i) {
            child.style.transitionDelay = Math.min(i * 55, 400) + 'ms';
          });
        }
        el.classList.add('is-visible');
        io.unobserve(el);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
    revealEls.forEach(function (el) { io.observe(el); });
  }

  // Animated number counters ([data-count] with optional data-prefix/data-suffix)
  var counters = document.querySelectorAll('[data-count]');
  function runCounter(el) {
    var target = parseFloat(el.getAttribute('data-count')) || 0;
    var prefix = el.getAttribute('data-prefix') || '';
    var suffix = el.getAttribute('data-suffix') || '';
    if (prefersReduced) { el.textContent = prefix + target + suffix; return; }
    var start = performance.now(), dur = 1400;
    function tick(now) {
      var p = Math.min((now - start) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = prefix + Math.round(target * eased).toLocaleString() + suffix;
      if (p < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }
  if (counters.length) {
    if (prefersReduced || !('IntersectionObserver' in window)) {
      counters.forEach(runCounter);
    } else {
      var cio = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) { if (e.isIntersecting) { runCounter(e.target); cio.unobserve(e.target); } });
      }, { threshold: 0.5 });
      counters.forEach(function (el) { cio.observe(el); });
    }
  }

  // Magnetic pull on all gold CTAs (and anything tagged .magnetic)
  if (!prefersReduced && window.matchMedia('(pointer:fine)').matches) {
    document.querySelectorAll('.magnetic, .btn-primary').forEach(function (el) {
      el.classList.add('magnetic');
      el.addEventListener('mousemove', function (e) {
        var r = el.getBoundingClientRect();
        var mx = e.clientX - r.left - r.width / 2;
        var my = e.clientY - r.top - r.height / 2;
        el.style.transform = 'translate(' + (mx * 0.18) + 'px,' + (my * 0.28) + 'px)';
      });
      el.addEventListener('mouseleave', function () { el.style.transform = ''; });
    });

    // Cursor spotlight on every hoverable card
    document.querySelectorAll('.spotlight, .card-hover').forEach(function (el) {
      el.addEventListener('mousemove', function (e) {
        var r = el.getBoundingClientRect();
        el.style.setProperty('--mx', (e.clientX - r.left) + 'px');
        el.style.setProperty('--my', (e.clientY - r.top) + 'px');
      });
    });
  }

  // Live mesh-gradient hero (lightweight canvas — the static-friendly "shader")
  var canvas = document.getElementById('hero-canvas');
  if (canvas && !prefersReduced) {
    var ctx = canvas.getContext('2d');
    // Navy / gold / soft-blue light sources that drift around the hero
    var blobs = [
      { hue: 'rgba(200,169,110,0.85)', ax: 0.26, ay: 0.30, sx: 0.21, sy: 0.16, fx: 0.7, fy: 0.5, ph: 0.0, r: 0.62 },
      { hue: 'rgba(74,108,176,0.85)',  ax: 0.76, ay: 0.24, sx: 0.18, sy: 0.20, fx: 0.5, fy: 0.8, ph: 1.7, r: 0.66 },
      { hue: 'rgba(35,58,100,0.95)',   ax: 0.58, ay: 0.78, sx: 0.22, sy: 0.16, fx: 0.6, fy: 0.4, ph: 3.1, r: 0.60 },
      { hue: 'rgba(216,196,154,0.60)', ax: 0.36, ay: 0.62, sx: 0.16, sy: 0.18, fx: 0.9, fy: 0.7, ph: 4.6, r: 0.50 }
    ];
    var W, H, t = 0, raf = null, running = false;
    function resize() {
      // Render at low resolution; CSS blur smooths it — very cheap.
      var scale = 0.42;
      W = canvas.width = Math.max(1, Math.round(canvas.offsetWidth * scale));
      H = canvas.height = Math.max(1, Math.round(canvas.offsetHeight * scale));
    }
    function render() {
      ctx.clearRect(0, 0, W, H);
      ctx.globalCompositeOperation = 'lighter';
      for (var i = 0; i < blobs.length; i++) {
        var b = blobs[i];
        var x = (b.ax + b.sx * Math.sin(t * b.fx + b.ph)) * W;
        var y = (b.ay + b.sy * Math.cos(t * b.fy + b.ph)) * H;
        var rad = b.r * Math.max(W, H);
        var g = ctx.createRadialGradient(x, y, 0, x, y, rad);
        g.addColorStop(0, b.hue);
        g.addColorStop(1, 'rgba(0,0,0,0)');
        ctx.fillStyle = g;
        ctx.fillRect(0, 0, W, H);
      }
    }
    function loop() { if (!running) return; t += 0.004; render(); raf = requestAnimationFrame(loop); }
    function start() { if (!running) { running = true; loop(); } }
    function stop() { running = false; if (raf) cancelAnimationFrame(raf); }
    resize();
    window.addEventListener('resize', function () { resize(); render(); }, { passive: true });
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) {
        es.forEach(function (e) { e.isIntersecting ? start() : stop(); });
      }, { threshold: 0 }).observe(canvas);
    } else { start(); }
  }
})();
