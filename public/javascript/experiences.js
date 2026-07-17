import { escapeFields } from './utils.js';

export const experienceConfig = {
  url: 'public/json/experiences.json',
  id: 'experience-container',
  tpl: i => {
    escapeFields(i, ['title', 'subtitle', 'role', 'alt', 'link']);
    return `
    <a target="_blank" rel="noopener noreferrer" href="${i.link || '#'}" aria-label="查看 ${i.title} 的相關經歷">
      <div class="card">
        <img loading="lazy" src="${i.img}" alt="${i.alt}" width="200" height="60">
        <p> 
          ${i.title}<br/>
          ${i.subtitle ? i.subtitle + '<br/>' : ''}
          ${i.role}
        </p>
      </div>
    </a>`;
  },
  suffix: `
    <a target="_blank" rel="noopener noreferrer" href="https://t.me/lcngtai">
      <div class="friend-card">
        <div class="friend-avatar"><h1>+</h1></div>
        <p>揪我出門</p>
      </div>
    </a>`
};