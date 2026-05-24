export const adsConfig = {
  url: '/json/ads.json',
  id: 'ads-container',
  
  // 每一筆廣告資料的 HTML 模板
  tpl: a => `
    <div class="card">
      <img loading="lazy" src="${a.img}" alt="${a.alt}">
      <h3>${a.title}</h3>
      <p>${a.desc}</p>
    </div>`
};
