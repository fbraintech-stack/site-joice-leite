// === NAVBAR SCROLL ===
const navbar = document.getElementById('navbar');
let lastScroll = 0;

window.addEventListener('scroll', () => {
  const currentScroll = window.scrollY;
  if (currentScroll > 50) {
    navbar.classList.add('scrolled');
  } else {
    navbar.classList.remove('scrolled');
  }
  lastScroll = currentScroll;
}, { passive: true });

// === MOBILE MENU ===
const navToggle = document.getElementById('navToggle');
const navLinks = document.getElementById('navLinks');

navToggle.addEventListener('click', () => {
  navLinks.classList.toggle('active');
  navToggle.setAttribute('aria-expanded', navLinks.classList.contains('active'));
});

// Close menu on link click
navLinks.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => {
    navLinks.classList.remove('active');
  });
});

// === SMOOTH SCROLL FOR ANCHOR LINKS ===
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', (e) => {
    const href = anchor.getAttribute('href');
    if (href === '#') return;
    e.preventDefault();
    const target = document.querySelector(href);
    if (target) {
      target.scrollIntoView({ behavior: 'smooth' });
    }
  });
});

// === SCROLL REVEAL ANIMATION ===
const observerOptions = {
  threshold: 0.1,
  rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('revealed');
      observer.unobserve(entry.target);
    }
  });
}, observerOptions);

// Observe all animatable elements
document.querySelectorAll(
  '.problem-card, .service-card, .step-card, .testimonial-card, .contact-card, .section-header, .about-content, .lead-magnet-content'
).forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(24px)';
  el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
  observer.observe(el);
});

// Add revealed class styles
const style = document.createElement('style');
style.textContent = `
  .revealed {
    opacity: 1 !important;
    transform: translateY(0) !important;
  }
`;
document.head.appendChild(style);

// Respect reduced motion
if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  document.querySelectorAll('.problem-card, .service-card, .step-card, .testimonial-card, .contact-card, .section-header, .about-content, .lead-magnet-content').forEach(el => {
    el.style.opacity = '1';
    el.style.transform = 'none';
    el.style.transition = 'none';
  });
}

// === LEAD FORM (placeholder) ===
const leadForm = document.getElementById('leadForm');
if (leadForm) {
  leadForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const name = document.getElementById('leadName').value;
    const whatsapp = document.getElementById('leadWhatsapp').value;

    // Placeholder - replace with actual form handling
    alert(`Obrigada, ${name}! Em breve você receberá o guia no WhatsApp ${whatsapp}.`);
    leadForm.reset();
  });
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
