export const friendsConfig = {
  url: 'public/json/friends.json',
  id: 'friends-container',
  tpl: f => `
    <a target="_blank" href="${f.link}">
      <div class="friend-card">
        <div class="friend-avatar">
          <img loading="lazy" src="${f.avatar}" alt="${f.name}">
        </div>
        <p>${f.name}</p>
      </div>
    </a>`,
  suffix: `
    <a target="_blank" href="https://github.com/longtai-me/NEW-ME/pulls">
      <div class="friend-card">
        <div class="friend-avatar"><h1>+</h1></div>
        <p>缺你一個</p>
      </div>
    </a>`
};