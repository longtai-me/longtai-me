import { escapeFields } from './utils.js';

// 專業證書預設展開，其餘課程證書收在「查看全部」後面
const PRO_KEYWORD = 'Professional Certificate';

/**
 * 單張證書卡片，沿用既有的 .card 樣式
 * @param {Object} c - 證書資料
 * @param {boolean} extra - 是否為預設收合的課程證書
 * @returns {string}
 */
function certCard(c, extra = false) {
  escapeFields(c, ['name', 'organization', 'date', 'link']);
  return `
    <a target="_blank" rel="noopener noreferrer" href="${c.link || '#'}" aria-label="驗證證書：${c.name}"${extra ? ' data-cert-extra hidden' : ''}>
      <div class="card cert-card">
        <div>
          <div class="cert-head">
            <span class="cert-label">CERTIFICATE</span>
            <span class="cert-date">${c.date}</span>
          </div>
          <h3>${c.name}</h3>
        </div>
        <div class="cert-foot">
          <span>${c.organization}</span>
          <span class="cert-verify">Verify &#8599;</span>
        </div>
      </div>
    </a>`;
}

export const certificateConfig = {
  url: 'public/json/certificate.json',
  id: 'certificate-container',

  render(data, el) {
    const featured = data.filter(c => (c.name || '').includes(PRO_KEYWORD));
    const extras = data.filter(c => !(c.name || '').includes(PRO_KEYWORD));

    el.innerHTML =
      featured.map(c => certCard(c)).join('') +
      extras.map(c => certCard(c, true)).join('');

    const count = document.getElementById('certificate-count');
    if (count) count.textContent = `${data.length} 張`;

    const toggle = document.getElementById('certificate-toggle');
    if (!toggle || !extras.length) return;

    const label = toggle.querySelector('.section-toggle-label');
    const action = toggle.querySelector('.section-toggle-action');
    const extraCards = el.querySelectorAll('a[data-cert-extra]');
    let expanded = false;

    const sync = () => {
      extraCards.forEach(a => { a.hidden = !expanded; });
      toggle.setAttribute('aria-expanded', String(expanded));
      label.textContent = expanded
        ? `已顯示全部 ${data.length} 張證書`
        : `另有 ${extras.length} 張課程證書`;
      action.textContent = expanded ? '收合 ←' : '查看全部 →';
    };

    toggle.addEventListener('click', () => {
      expanded = !expanded;
      sync();
    });

    toggle.hidden = false;
    sync();
  }
};
