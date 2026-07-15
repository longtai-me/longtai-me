export const friendsConfig = {
  url: 'public/json/friends.json',
  id: 'friends-container',
  tpl: f => `
    <a target="_blank" href="${f.link}" aria-label="前往大電神 ${f.name} 的網站">
      <div class="friend-card">
        <div class="friend-avatar">
          <img loading="lazy" src="${f.avatar}" alt="${f.name}" width="70" height="70">
        </div>
        <p>${f.name}</p>
      </div>
    </a>`,
  suffix: `
    <a target="_blank" href="https://github.com/longtai-me/longtai-me/pulls">
      <div class="friend-card">
        <div class="friend-avatar"><h1>+</h1></div>
        <p>缺你一個</p>
      </div>
    </a>`
};
