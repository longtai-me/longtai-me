import { escapeFields } from './utils.js';

export const adsConfig = {
  url: 'public/json/ads.json',
  id: 'ads-container',

  // 每一筆廣告資料的 HTML 模板
  tpl: a => {
    escapeFields(a, ['title', 'desc', 'alt']);
    const specialClass = a.specialStyle ? ` data-special="${a.specialStyle}"` : '';
    return `
    <div class="card"${specialClass}>
      <img loading="lazy" src="${a.img}" alt="${a.alt}" width="200" height="60">
      <h3>${a.title}</h3>
      <p>${a.desc}</p>
    </div>`;
  }
};