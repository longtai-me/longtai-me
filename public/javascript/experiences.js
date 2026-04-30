export const experienceConfig = {
  url: '/public/json/experiences.json',
  id: 'experience-container',
  tpl: i => `
    <a target="_blank" href="${i.link || '#'}">
      <div class="card">
        <img loading="lazy" src="${i.img}" alt="${i.alt}">
        <p>
          ${i.title}<br/>
          ${i.subtitle ? i.subtitle + '<br/>' : ''}
          ${i.role}
        </p>
      </div>
    </a>`
};