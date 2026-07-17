/**
 * 將字串轉義為安全的 HTML，避免 XSS
 * 使用字元碼避免被編輯器自動轉換
 * @param {string} str
 * @returns {string}
 */
export function escapeHtml(str = '') {
  return String(str)
    .replace(/\x26/g, '\x26amp;')   // &
    .replace(/\x3C/g, '\x26lt;')    // <
    .replace(/\x3E/g, '\x26gt;')    // >
    .replace(/\x22/g, '\x26quot;')  // "
    .replace(/\x27/g, '\x26#39;');  // '
}

/**
 * 將物件中的指定欄位轉義為安全 HTML
 * @param {Object} obj
 * @param {string[]} fields
 * @returns {Object} 回傳原物件（已就地修改）
 */
export function escapeFields(obj, fields) {
  for (const f of fields) {
    if (obj[f] !== undefined && obj[f] !== null) {
      obj[f] = escapeHtml(obj[f]);
    }
  }
  return obj;
}