import { apiBlob } from './api.js';

export const extOf = (name = '') => (name.includes('.') ? name.split('.').pop().toLowerCase() : '');

const TEXT_EXT = new Set([
  'txt', 'log', 'json', 'xml', 'csv', 'tsv', 'yml', 'yaml', 'toml', 'ini', 'env', 'conf', 'cfg',
  'js', 'jsx', 'ts', 'tsx', 'py', 'java', 'c', 'h', 'cpp', 'cs', 'go', 'rs', 'rb', 'php', 'sh',
  'sql', 'css', 'html', 'htm', 'tex', 'rst',
]);
const TEXT_TYPES = [
  'application/json', 'application/xml', 'application/javascript', 'application/x-yaml',
  'application/x-sh', 'application/sql', 'application/x-httpd-php',
];

/** What kind of in-browser preview can we offer? null = download only. */
export function previewKind({ filename, content_type }) {
  const ext = extOf(filename);
  const type = (content_type || '').toLowerCase();
  if (ext === 'md' || ext === 'markdown' || type === 'text/markdown') return 'markdown';
  if (type.startsWith('image/')) return 'image';
  if (type === 'application/pdf' || ext === 'pdf') return 'pdf';
  if (type.startsWith('video/')) return 'video';
  if (type.startsWith('audio/')) return 'audio';
  if (type.startsWith('text/') || TEXT_TYPES.includes(type) || TEXT_EXT.has(ext)) return 'text';
  return null;
}

export function saveBlob(blob, filename) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

export async function downloadDocument(doc) {
  saveBlob(await apiBlob(`/document/${doc.id}`), doc.filename);
}
