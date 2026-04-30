export function initTyping(text = "Longtai", speed = 180) {
  const target = document.querySelector(".typing");
  if (!target) return;
  
  let i = 0;
  function type() {
    if (i < text.length) {
      target.textContent += text.charAt(i);
      i++;
      setTimeout(type, speed);
    }
  }
  type();
}

// 元素進入視線動畫 (Reveal Effect)
export function initScrollReveal() {
  const reveals = document.querySelectorAll('.card, .friend-card, .social-icon');
  
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('active');
      }
    });
  }, { threshold: 0.1 });

  reveals.forEach(el => {
    el.classList.add('reveal');
    observer.observe(el);
  });
}

// Header 縮減效果
export function initHeaderScroll() {
  const header = document.querySelector("header");
  if (!header) return;

  window.addEventListener("scroll", () => {
    header.style.padding = window.scrollY > 50 ? "10px 0" : "0";
  });
}