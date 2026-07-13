export const adsConfig = {
  url: 'public/json/ads.json',
  id: 'ads-container',
  
  // 每一筆廣告資料的 HTML 模板
  tpl: a => `
    <div class="card">
      <img loading="lazy" src="${a.img}" alt="${a.alt}" width="200" height="60">
      <h3>${a.title}</h3>
      <p>${a.desc}</p>
    </div>`
};