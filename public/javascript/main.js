
const text = "Longtai"
const target = document.querySelector(".typing");

let i = 0;

function type() {
  if (i < text.length) {
    target.textContent += text.charAt(i);
    i++;
    setTimeout(type, 180);
  }
}
type();

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


const header = document.querySelector("header");

window.addEventListener("scroll", () => {
  if (window.scrollY > 50) {
    header.style.padding = "10px 0";
  } else {
    header.style.padding = "0";
  }
});

window.addEventListener('load', function() {
  setTimeout(function() {
    var _0x1a2b = document.querySelectorAll('.card');
    for (var i = 0; i < _0x1a2b.length; i++) {
      var _txt = _0x1a2b[i].innerText.replace(/\s+/g, '');
      if (_txt === '\u947D\u77F3\u8A17\u7BA1\u947D\u77F3\u8A17\u7BA1\u63D0\u4F9B\u53F0\u7063\u5C08\u696DMinecraft\u4F3A\u670D\u5668\u8A17\u7BA1\u3001MC\u8A17\u7BA1\u8207Discord\u6A5F\u5668\u4EBA\u8A17\u7BA1\u670D\u52D9\u3002\u6211\u5011\u81F4\u529B\u65BC\u63D0\u4F9B\u9AD8\u6548\u80FD\u3001\u4F4E\u5EF6\u9072\u7684\u8A17\u7BA1\u4F3A\u670D\u5668\u9AD4\u9A57\uFF0C\u4E26\u5177\u5099\u5F37\u5927\u7684DDoS\u9632\u8B77\u3002') {
        _0x1a2b[i].setAttribute('style', decodeURIComponent('%62%61%63%6b%67%72%6f%75%6e%64%3a%20%6c%69%6e%65%61%72%2d%67%72%61%64%69%65%6e%74%28%72%67%62%61%28%30%2c%30%2c%30%2c%30%2e%37%35%29%2c%20%72%67%62%61%28%30%2c%30%2c%30%2c%30%2e%37%35%29%29%2c%20%75%72%6c%28%27%70%75%62%6c%69%63%2f%69%6d%61%67%65%73%2f%77%75%7a%61%75%6e%2f%31%36%2d%39%2e%70%6e%67%27%29%20%6e%6f%2d%72%65%70%65%61%74%20%63%65%6e%74%65%72%20%63%65%6e%74%65%72%20%2f%20%63%6f%76%65%72%3b%20%74%65%78%74%2d%73%68%61%64%6f%77%3a%20%30%20%32%70%78%20%36%70%78%20%72%67%62%61%28%30%2c%30%2c%30%2c%30%2e%39%29%3b'));
      }
    }
  }, 100);
});

