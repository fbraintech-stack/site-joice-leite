// ============================================
// JOICE LEITE — ANIMATION SYSTEM
// Premium motion design: stagger reveals,
// parallax, counters, tilt cards, magnetic CTAs
// ============================================

const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

// === NAVBAR ===
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 50);
}, { passive: true });

// === MOBILE MENU (SIDEBAR) ===
const navToggle = document.getElementById('navToggle');
const navLinks = document.getElementById('navLinks');
const navOverlay = document.getElementById('navOverlay');

function toggleMenu(open) {
  const isOpen = typeof open === 'boolean' ? open : !navLinks.classList.contains('active');
  navLinks.classList.toggle('active', isOpen);
  navToggle.classList.toggle('open', isOpen);
  navOverlay?.classList.toggle('active', isOpen);
  document.body.style.overflow = isOpen ? 'hidden' : '';
}

navToggle.addEventListener('click', () => toggleMenu());
navOverlay?.addEventListener('click', () => toggleMenu(false));

navLinks.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => toggleMenu(false));
});

// === SMOOTH SCROLL ===
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', (e) => {
    const href = anchor.getAttribute('href');
    if (href === '#') return;
    e.preventDefault();
    document.querySelector(href)?.scrollIntoView({ behavior: 'smooth' });
  });
});

// === HERO STAGGERED ENTRANCE ===
function animateHero() {
  if (prefersReducedMotion) return;

  const elements = [
    { el: '.hero-badge', delay: 200 },
    { el: '.hero-title', delay: 500 },
    { el: '.hero-subtitle', delay: 800 },
    { el: '.hero-actions', delay: 1100 },
    { el: '.hero-trust', delay: 1400 },
  ];

  elements.forEach(({ el, delay }) => {
    const node = document.querySelector(el);
    if (!node) return;
    node.style.opacity = '0';
    node.style.transform = 'translateY(30px)';
    node.style.transition = 'none';

    setTimeout(() => {
      node.style.transition = 'opacity 0.8s cubic-bezier(0.16, 1, 0.3, 1), transform 0.8s cubic-bezier(0.16, 1, 0.3, 1)';
      node.style.opacity = '1';
      node.style.transform = 'translateY(0)';
    }, delay);
  });
}

// === TEXT ACCENT SHIMMER ===
function initAccentShimmer() {
  if (prefersReducedMotion) return;
  const accent = document.querySelector('.text-accent');
  if (!accent) return;

  setTimeout(() => {
    accent.classList.add('shimmer-active');
  }, 1800);
}

// === SCROLL REVEAL WITH STAGGER ===
function initScrollReveal() {
  if (prefersReducedMotion) {
    document.querySelectorAll('[data-reveal]').forEach(el => {
      el.style.opacity = '1';
      el.style.transform = 'none';
    });
    return;
  }

  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const delay = parseInt(el.dataset.revealDelay || '0');
        const direction = el.dataset.reveal || 'up';

        setTimeout(() => {
          el.classList.add('revealed');
        }, delay);

        revealObserver.unobserve(el);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -60px 0px' });

  // Tag all revealable elements
  const revealGroups = [
    { selector: '.section-header', reveal: 'up' },
    { selector: '.problem-card', reveal: 'up', stagger: 80 },
    { selector: '.problems-cta', reveal: 'up' },
    { selector: '.service-card', reveal: 'up', stagger: 150 },
    { selector: '.services-cta', reveal: 'up' },
    { selector: '.step-card', reveal: 'up', stagger: 200 },
    { selector: '.step-connector', reveal: 'fade', stagger: 300 },
    { selector: '.about-image', reveal: 'left' },
    { selector: '.about-text', reveal: 'right', fixedDelay: 200 },
    { selector: '.testimonial-card', reveal: 'up', stagger: 150 },
    { selector: '.lead-magnet-text', reveal: 'left' },
    { selector: '.lead-magnet-form', reveal: 'right' },
    { selector: '.contact-card', reveal: 'up', stagger: 120 },
  ];

  revealGroups.forEach(group => {
    const elements = document.querySelectorAll(group.selector);
    elements.forEach((el, i) => {
      el.dataset.reveal = group.reveal;
      el.dataset.revealDelay = group.fixedDelay
        ? group.fixedDelay.toString()
        : group.stagger ? (i * group.stagger).toString() : '0';
      revealObserver.observe(el);
    });
  });
}

// === ANIMATED COUNTER ===
function initCounters() {
  if (prefersReducedMotion) return;

  const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCounter(entry.target);
        counterObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  document.querySelectorAll('[data-count]').forEach(el => {
    counterObserver.observe(el);
  });
}

function animateCounter(el) {
  const target = parseInt(el.dataset.count);
  const duration = 2000;
  const start = performance.now();
  const prefix = el.dataset.countPrefix || '';
  const suffix = el.dataset.countSuffix || '';

  function update(now) {
    const elapsed = now - start;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 4); // ease-out quart
    const current = Math.round(eased * target);

    el.textContent = prefix + current + suffix;

    if (progress < 1) requestAnimationFrame(update);
  }

  requestAnimationFrame(update);
}

// === CARD TILT 3D EFFECT ===
function initCardTilt() {
  if (prefersReducedMotion) return;

  document.querySelectorAll('.service-card, .contact-card').forEach(card => {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;

      const rotateX = ((y - centerY) / centerY) * -4;
      const rotateY = ((x - centerX) / centerX) * 4;

      card.style.transform = `perspective(800px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-4px)`;
    });

    card.addEventListener('mouseleave', () => {
      card.style.transform = '';
      card.style.transition = 'transform 0.5s cubic-bezier(0.16, 1, 0.3, 1)';
      setTimeout(() => { card.style.transition = ''; }, 500);
    });
  });
}

// === MAGNETIC BUTTON EFFECT ===
function initMagneticButtons() {
  if (prefersReducedMotion) return;

  document.querySelectorAll('.btn-primary').forEach(btn => {
    btn.addEventListener('mousemove', (e) => {
      const rect = btn.getBoundingClientRect();
      const x = e.clientX - rect.left - rect.width / 2;
      const y = e.clientY - rect.top - rect.height / 2;

      btn.style.transform = `translate(${x * 0.15}px, ${y * 0.15}px)`;
    });

    btn.addEventListener('mouseleave', () => {
      btn.style.transform = '';
      btn.style.transition = 'transform 0.4s cubic-bezier(0.16, 1, 0.3, 1)';
      setTimeout(() => { btn.style.transition = ''; }, 400);
    });
  });
}

// === PARALLAX SCROLL ===
function initParallax() {
  if (prefersReducedMotion) return;

  const orbs = document.querySelectorAll('.hero-orb');
  const lines = document.querySelectorAll('.hero-line');

  window.addEventListener('scroll', () => {
    const scrollY = window.scrollY;
    if (scrollY > window.innerHeight) return; // only in hero

    orbs.forEach((orb, i) => {
      const speed = 0.05 + (i * 0.02);
      orb.style.transform = `translateY(${scrollY * speed}px)`;
    });

    lines.forEach((line, i) => {
      const speed = 0.03 + (i * 0.015);
      const baseRotate = i === 0 ? 25 : -15;
      line.style.transform = `rotate(${baseRotate}deg) translateY(${scrollY * speed}px)`;
    });
  }, { passive: true });
}

// === STEP CONNECTOR DRAW ANIMATION ===
function initStepConnectors() {
  if (prefersReducedMotion) return;

  document.querySelectorAll('.step-connector svg path').forEach(path => {
    const length = path.getTotalLength();
    path.style.strokeDasharray = length;
    path.style.strokeDashoffset = length;
    path.style.transition = 'stroke-dash-offset 1s ease';
  });

  const connectorObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.querySelectorAll('path').forEach(path => {
          path.style.transition = 'stroke-dashoffset 1.2s cubic-bezier(0.16, 1, 0.3, 1)';
          path.style.strokeDashoffset = '0';
        });
        connectorObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  document.querySelectorAll('.step-connector').forEach(el => {
    connectorObserver.observe(el);
  });
}

// === GLOW FOLLOW CURSOR ON CARDS ===
function initGlowFollow() {
  if (prefersReducedMotion) return;

  document.querySelectorAll('.service-card, .testimonial-card').forEach(card => {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      card.style.setProperty('--glow-x', `${x}px`);
      card.style.setProperty('--glow-y', `${y}px`);
    });
  });
}

// === NAVBAR LINK UNDERLINE ANIMATION ===
function initNavUnderline() {
  document.querySelectorAll('.nav-links a:not(.nav-cta)').forEach(link => {
    link.addEventListener('mouseenter', () => link.classList.add('hover'));
    link.addEventListener('mouseleave', () => link.classList.remove('hover'));
  });
}

// === SCROLL PROGRESS BAR ===
function initScrollProgress() {
  const bar = document.createElement('div');
  bar.className = 'scroll-progress';
  document.body.appendChild(bar);

  window.addEventListener('scroll', () => {
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = (scrollTop / docHeight) * 100;
    bar.style.width = `${progress}%`;
  }, { passive: true });
}

// === WHATSAPP PHONE MASK ===
const phoneInput = document.getElementById('leadWhatsapp');
if (phoneInput) {
  phoneInput.addEventListener('input', (e) => {
    let value = e.target.value.replace(/\D/g, '');
    if (value.length > 11) value = value.slice(0, 11);
    if (value.length > 6) {
      value = `(${value.slice(0, 2)}) ${value.slice(2, 7)}-${value.slice(7)}`;
    } else if (value.length > 2) {
      value = `(${value.slice(0, 2)}) ${value.slice(2)}`;
    } else if (value.length > 0) {
      value = `(${value}`;
    }
    e.target.value = value;
  });
}

// === LEAD FORM ===
const leadForm = document.getElementById('leadForm');
if (leadForm) {
  leadForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const name = document.getElementById('leadName').value;
    const whatsapp = document.getElementById('leadWhatsapp').value;
    const btn = leadForm.querySelector('button');
    const originalHTML = btn.innerHTML;

    btn.textContent = 'Enviando...';
    btn.disabled = true;

    setTimeout(() => {
      btn.textContent = 'Pronto!';
      btn.style.background = 'linear-gradient(135deg, #2ecc71, #27ae60)';

      // Popup de agradecimento
      showThankYouPopup(name, () => {
        // Download do PDF ao clicar OK
        const link = document.createElement('a');
        link.href = 'assets/guia-7-armadilhas.pdf';
        link.download = '7-Armadilhas-Imoveis-Joice-Leite.pdf';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        // Resetar form
        leadForm.reset();
        btn.innerHTML = originalHTML;
        btn.style.background = '';
        btn.disabled = false;
      });
    }, 1200);
  });
}

function showThankYouPopup(name, onClose) {
  // Overlay
  const overlay = document.createElement('div');
  overlay.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(11,17,32,0.85);z-index:10000;display:flex;align-items:center;justify-content:center;opacity:0;transition:opacity 0.3s ease;backdrop-filter:blur(4px)';

  // Modal
  const modal = document.createElement('div');
  modal.style.cssText = 'background:linear-gradient(145deg,#111B30,#0B1120);border:1px solid #C4956A;border-radius:16px;padding:40px 36px;max-width:420px;width:90%;text-align:center;transform:scale(0.9);transition:transform 0.3s cubic-bezier(0.16,1,0.3,1);box-shadow:0 20px 60px rgba(0,0,0,0.5)';

  modal.innerHTML = `
    <div style="width:56px;height:56px;border-radius:50%;background:linear-gradient(135deg,#C4956A,#8B6A4A);display:flex;align-items:center;justify-content:center;margin:0 auto 20px">
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
    </div>
    <h3 style="font-family:'Cinzel',serif;color:#C4956A;font-size:1.3rem;margin:0 0 12px">Obrigada, ${name}!</h3>
    <p style="font-family:'Inter',sans-serif;color:#F1F0EE;font-size:0.95rem;line-height:1.6;margin:0 0 8px">Seu guia <strong>"7 Armadilhas Escondidas em Imóveis Perfeitos"</strong> está pronto.</p>
    <p style="font-family:'Inter',sans-serif;color:#A0A0B0;font-size:0.85rem;line-height:1.5;margin:0 0 24px">Clique no botão abaixo para baixar o PDF.</p>
    <button id="popupDownloadBtn" style="font-family:'Inter',sans-serif;background:linear-gradient(135deg,#C4956A,#A07B55);color:#0B1120;border:none;padding:14px 36px;border-radius:8px;font-size:1rem;font-weight:600;cursor:pointer;transition:transform 0.2s ease,box-shadow 0.2s ease;box-shadow:0 4px 15px rgba(196,149,106,0.3)">
      Baixar meu guia grátis
    </button>
  `;

  overlay.appendChild(modal);
  document.body.appendChild(overlay);
  document.body.style.overflow = 'hidden';

  // Animate in
  requestAnimationFrame(() => {
    overlay.style.opacity = '1';
    modal.style.transform = 'scale(1)';
  });

  // Hover effect no botão
  const dlBtn = document.getElementById('popupDownloadBtn');
  dlBtn.addEventListener('mouseenter', () => {
    dlBtn.style.transform = 'translateY(-2px)';
    dlBtn.style.boxShadow = '0 6px 20px rgba(196,149,106,0.4)';
  });
  dlBtn.addEventListener('mouseleave', () => {
    dlBtn.style.transform = '';
    dlBtn.style.boxShadow = '0 4px 15px rgba(196,149,106,0.3)';
  });

  // Close on button click
  dlBtn.addEventListener('click', () => {
    overlay.style.opacity = '0';
    modal.style.transform = 'scale(0.9)';
    setTimeout(() => {
      document.body.removeChild(overlay);
      document.body.style.overflow = '';
      if (onClose) onClose();
    }, 300);
  });
}

// === FAQ ACCORDION ===
function initFaqAccordion() {
  document.querySelectorAll('.faq-question').forEach((btn) => {
    btn.addEventListener('click', () => {
      const item = btn.closest('.faq-item');
      if (!item) return;
      const isActive = item.classList.contains('active');
      document.querySelectorAll('.faq-item.active').forEach((active) => {
        active.classList.remove('active');
        const q = active.querySelector('.faq-question');
        if (q) q.setAttribute('aria-expanded', 'false');
      });
      if (!isActive) {
        item.classList.add('active');
        btn.setAttribute('aria-expanded', 'true');
      }
    });
  });
}

// === INIT ALL ===
document.addEventListener('DOMContentLoaded', () => {
  animateHero();
  initAccentShimmer();
  initScrollReveal();
  initCounters();
  initCardTilt();
  initMagneticButtons();
  initParallax();
  initStepConnectors();
  initGlowFollow();
  initNavUnderline();
  initScrollProgress();
  initFaqAccordion();
});
