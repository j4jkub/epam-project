/** Backend returns optional fields; give the UI predictable shapes. */
export function normalizeProject(p) {
  const ownerId = p.owner?.id;
  return {
    ...p,
    description: p.description || '',
    owner: p.owner || null,
    participants: (p.participants || []).filter((u) => u.id !== ownerId),
    is_owner: !!p.is_owner,
  };
}

const esc = (s) =>
  s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

const inline = (t) =>
  esc(t)
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/\*([^*]+)\*/g, '<em>$1</em>')
    .replace(/\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/g, '<a href="$2" target="_blank" rel="noreferrer">$1</a>');

/* Small, safe markdown renderer: headings, lists, quotes, code, bold, italic, links */
export function renderMarkdown(src) {
  let html = '';
  let list = false;
  let code = false;
  for (const raw of src.split('\n')) {
    if (raw.startsWith('```')) {
      html += code ? '</code></pre>' : '<pre><code>';
      code = !code;
      continue;
    }
    if (code) {
      html += esc(raw) + '\n';
      continue;
    }
    const li = raw.match(/^\s*[-*]\s+(.*)/);
    if (li) {
      if (!list) { html += '<ul>'; list = true; }
      html += `<li>${inline(li[1])}</li>`;
      continue;
    }
    if (list) { html += '</ul>'; list = false; }
    const h = raw.match(/^(#{1,3})\s+(.*)/);
    if (h) { html += `<h${h[1].length}>${inline(h[2])}</h${h[1].length}>`; continue; }
    if (raw.startsWith('> ')) { html += `<blockquote>${inline(raw.slice(2))}</blockquote>`; continue; }
    if (raw.trim() === '') continue;
    html += `<p>${inline(raw)}</p>`;
  }
  if (list) html += '</ul>';
  if (code) html += '</code></pre>';
  return html;
}
