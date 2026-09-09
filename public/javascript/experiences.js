import { escapeFields } from './utils.js';

const CTA_LINK = 'https://t.me/lcngtai';

/**
 * 年表的一列
 * @param {Object} e - 單筆經歷
 * @returns {string}
 */
function row(e) {
  escapeFields(e, ['title', 'subtitle', 'role', 'link']);
  return `
      <li>
        <a class="timeline-row" target="_blank" rel="noopener noreferrer" href="${e.link || '#'}" aria-label="查看 ${e.title} 的相關經歷">
          <span class="timeline-title">${e.title}</span>
          <span class="timeline-sub">${e.subtitle || ''}</span>
          <span class="timeline-role">${e.role}</span>
        </a>
      </li>`;
}

/**
 * 一個年份分組
 * @param {string} year
 * @param {Object[]} items
 * @param {boolean} collapsed - 是否預設收合
 * @returns {string}
 */
function group(year, items, collapsed) {
  return `
    <div class="timeline-group${collapsed ? ' timeline-group--extra' : ''}"${collapsed ? ' hidden' : ''}>
      <h3 class="timeline-year">${year}</h3>
      <ul class="timeline-rows">${items.map(row).join('')}</ul>
    </div>`;
}

// 年表結尾固定放的邀約入口
function cta() {
  return `
    <div class="timeline-group">
      <div></div>
      <ul class="timeline-rows">
        <li>
          <a class="timeline-row timeline-row--cta" target="_blank" rel="noopener noreferrer" href="${CTA_LINK}">
            <span class="timeline-title">揪我出門</span>
            <span class="timeline-sub">有活動歡迎找我</span>
            <span class="timeline-role">Telegram →</span>
          </a>
        </li>
      </ul>
    </div>`;
}

export const experienceConfig = {
  url: 'public/json/experiences.json',
  id: 'experience-container',

  render(data, el) {
    // 依年份分組，新的年份在前（JSON 內的順序不保證排序）
    const byYear = new Map();
    for (const e of data) {
      const year = String(e.years);
      if (!byYear.has(year)) byYear.set(year, []);
      byYear.get(year).push(e);
    }
    const years = [...byYear.keys()].sort((a, b) => b.localeCompare(a));
    if (!years.length) return;

    // 今年的展開，其餘收合；今年還沒有紀錄時改為展開最新的一年
    const thisYear = String(new Date().getFullYear());
    const openYear = byYear.has(thisYear) ? thisYear : years[0];
    const hiddenCount = data.length - byYear.get(openYear).length;

    el.innerHTML =
      years.map(y => group(y, byYear.get(y), y !== openYear)).join('') + cta();

    const count = document.getElementById('experience-count');
    if (count) {
      count.textContent = `${data.length} 筆 · ${years[years.length - 1]}–${years[0]}`;
    }

    const toggle = document.getElementById('experience-toggle');
    if (!toggle || !hiddenCount) return;

    const label = toggle.querySelector('.section-toggle-label');
    const action = toggle.querySelector('.section-toggle-action');
    const extras = el.querySelectorAll('.timeline-group--extra');
    let expanded = false;

    const sync = () => {
      extras.forEach(g => { g.hidden = !expanded; });
      toggle.setAttribute('aria-expanded', String(expanded));
      label.textContent = expanded
        ? `已顯示全部 ${data.length} 筆經歷`
        : `另有 ${hiddenCount} 筆其他年份的經歷`;
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
