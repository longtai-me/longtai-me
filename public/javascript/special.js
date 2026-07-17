/**
 * 依據 data-special 屬性套用特殊樣式
 * 取代原本用整段文字比對的脆弱做法
 */
export function applySpecialStyles() {
  const specialCards = document.querySelectorAll('[data-special]');
  
  specialCards.forEach(card => {
    const style = card.dataset.special;
    if (style === 'diamondhost') {
      card.style.background = "linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.75)), url('public/images/ads/16-9.webp') no-repeat center center / cover";
      card.style.textShadow = "0 2px 6px rgba(0,0,0,0.9)";
    }
  });
}