export function applySpecialStyles() {
  const cards = document.querySelectorAll('.card');
  const targetText = '鑽石託管鑽石託管提供台灣專業Minecraft伺服器託管、MC託管與Discord機器人託管服務。我們致力於提供高效能、低延遲的託管伺服器體驗，並具備強大的DDoS防護。';
  
  cards.forEach(card => {
    const cleanText = card.innerText.replace(/\s+/g, '');
    if (cleanText === targetText) {
      card.style.background = "linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.75)), url('public/images/wuzaun/16-9.png') no-repeat center center / cover";
      card.style.textShadow = "0 2px 6px rgba(0,0,0,0.9)";
    }
  });
}