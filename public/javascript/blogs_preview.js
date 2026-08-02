import { escapeFields } from './utils.js';

export const blogsConfig = {
  url: 'public/json/blogs.json',
  id: 'blogs-container',
  tpl: b => {
    escapeFields(b, ['id', 'title']);
    return `
    <a href="/blogs.html?post=${encodeURIComponent(b.id || b.title)}" aria-label="閱讀文章：${b.title}">
      <div class="card" style="text-align: left; justify-content: space-between;">
        <div>
          <div style="font-size: 0.85rem; color: var(--primary); font-weight: 600; margin-bottom: 8px; letter-spacing: 0.05em;">ARTICLE</div>
          <h3 style="margin: 0 0 10px 0; font-size: 1.15rem; line-height: 1.4; color: #ffffff;">${b.title}</h3>
        </div>
        <div style="display: flex; align-items: center; justify-content: space-between; margin-top: 15px; font-size: 0.9rem; color: var(--muted);">
          <span>閱讀全文</span>
          <span style="font-size: 1.1rem; color: var(--primary);">&rarr;</span>
        </div>
      </div>
    </a>`;
  },
  suffix: `
    <a href="/blogs.html" aria-label="查看所有部落格文章">
      <div class="friend-card" style="min-height: 120px;">
        <div class="friend-avatar"><h1>+</h1></div>
        <p>所有文章</p>
      </div>
    </a>`
};
