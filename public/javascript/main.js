import { experienceConfig } from './experiences.js';
import { friendsConfig } from './friends.js';
import { supportConfig } from './support.js';
import { adsConfig } from './ads.js';
import { initTyping, initScrollReveal, initHeaderScroll } from './ui.js';
import { applySpecialStyles } from './special.js';

document.addEventListener('DOMContentLoaded', () => {
  // 1. 初始化 UI 效果
  initTyping("Longtai", 180);
  initScrollReveal();
  initHeaderScroll();

  // 2. 處理資料渲染
  const configs = [experienceConfig, friendsConfig, supportConfig, adsConfig];
  
  // 建立一個 Promise 陣列來追蹤所有資料是否載入完成
  const fetchPromises = configs.map(conf => {
    const el = document.getElementById(conf.id);
    if (!el) return Promise.resolve();

    return fetch(conf.url)
      .then(res => res.json())
      .then(data => {
        el.innerHTML = data.map(conf.tpl).join('') + (conf.suffix || '');
      })
      .catch(err => {
        console.error(`載入 ${conf.url} 失敗:`, err);
        el.innerHTML = `<p style="color:var(--muted); text-align:center;">暫時無法載入</p>`;
      });
  });

  // 3. 當所有內容載入後，執行特定樣式檢查與動畫重新掃描
  Promise.all(fetchPromises).then(() => {
    applySpecialStyles(); // 處理鑽石託管樣式
    initScrollReveal();   // 針對動態生成的卡片再次執行監聽
  });
});

// 全域圖片錯誤處理
window.addEventListener('error', (e) => {
  if (e.target.tagName.toLowerCase() !== 'img') return;
  const img = e.target;
  if (img.dataset.errorAttempted) return;
  img.dataset.errorAttempted = "true";
  img.src = img.closest('.friend-avatar') 
    ? 'https://www.gravatar.com/avatar/00000000?d=mp&s=200' 
    : '/public/images/events/nopng.png';
}, true);