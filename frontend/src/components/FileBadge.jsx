import { extOf } from '../files.js';

export default function FileBadge({ filename }) {
  const ext = extOf(filename).slice(0, 4) || 'file';
  return <span className="file-badge">{ext}</span>;
}
