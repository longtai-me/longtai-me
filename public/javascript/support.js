export const supportConfig = {
  url: 'public/json/support.json',
  id: 'support-container',
  
  // 每一筆贊助/支持項目的 HTML 模板
  tpl: s => `
    <div class="card">
      <img loading="lazy" src="${s.img}" alt="${s.alt}">
      <p>
        ${s.title}<br/>
        ${s.subtitle ? s.subtitle + '<br/>' : ''}
        ${s.desc}
      </p>
    </div>`
};