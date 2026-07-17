/**
 * 打字效果：使用 IntersectionObserver 在元素進入視窗時觸發，離開再回來可重播
 * @param {string} text - 要打出的文字
 * @param {number} speed - 每字毫秒數
 */
export function initTyping(text = "Longtai", speed = 180) {
  const target = document.querySelector(".typing");
  if (!target) return;

  let i = 0;
  let timer = null;
  let started = false;

  function type() {
    if (i < text.length) {
      target.textContent += text.charAt(i);
      i++;
      timer = setTimeout(type, speed);
    }
  }

  function reset() {
    clearTimeout(timer);
    i = 0;
    target.textContent = '';
    started = false;
  }

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting && !started) {
        started = true;
        type();
      } else if (!entry.isIntersecting) {
        reset();
      }
    });
  }, { threshold: 0.5 });

  observer.observe(target);
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