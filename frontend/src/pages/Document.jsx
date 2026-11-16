import { useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { api, apiBlob } from '../api.js';
import { previewKind, saveBlob } from '../files.js';
import { normalizeProject, renderMarkdown } from '../utils.js';

const MAX_TEXT = 1_000_000; // characters shown in the text preview

export default function Document() {
  const { id, docId } = useParams();
  const navigate = useNavigate();
  const [project, setProject] = useState(null);
  const [doc, setDoc] = useState(null);
  const [blob, setBlob] = useState(null);
  const [url, setUrl] = useState(null);
  const [text, setText] = useState(null);
  const [truncated, setTruncated] = useState(false);
  const [rawMarkdown, setRawMarkdown] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let cancelled = false;
    let objectUrl = null;
    setLoading(true);
    setError('');
    setUrl(null);
    setText(null);
    setBlob(null);

    (async () => {
      try {
        const [p, docs] = await Promise.all([api(`/project/${id}/info`), api(`/project/${id}/documents`)]);
        const d = docs.find((x) => String(x.id) === String(docId));
        if (!d) throw new Error('Document not found');
        if (cancelled) return;
        setProject(normalizeProject(p));
        setDoc(d);

        const kind = previewKind(d);
        if (kind) {
          const raw = await apiBlob(`/document/${docId}`);
          const b = new Blob([raw], { type: d.content_type || raw.type });
          if (cancelled) return;
          setBlob(b);
          if (kind === 'text' || kind === 'markdown') {
            const t = await b.text();
            if (cancelled) return;
            setTruncated(t.length > MAX_TEXT);
            setText(t.slice(0, MAX_TEXT));
          } else {
            objectUrl = URL.createObjectURL(b);
            setUrl(objectUrl);
          }
        }
      } catch (e) {
        if (!cancelled) setError(e.message);
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();

    return () => {
      cancelled = true;
      if (objectUrl) URL.revokeObjectURL(objectUrl);
    };
  }, [id, docId]);

  async function download() {
    try {
      saveBlob(blob || (await apiBlob(`/document/${docId}`)), doc.filename);
    } catch (e) {
      setError(e.message);
    }
  }

  async function remove() {
    if (!confirm(`Delete “${doc.filename}”? This can't be undone.`)) return;
    try {
      await api(`/document/${docId}`, { method: 'DELETE' });
      navigate(`/projects/${id}`);
    } catch (e) {
      setError(e.message);
    }
  }

  if (!doc) {
    return (
      <div className="container section">
        {error ? (
          <div className="empty">
            <h3>{error}</h3>
            <Link to={`/projects/${id}`} className="btn">Back to project</Link>
          </div>
        ) : (
          <p className="center-note">Loading…</p>
        )}
      </div>
    );
  }

  const kind = previewKind(doc);

  return (
    <div className="container doc-page">
      <div className="crumbs">
        <Link to="/projects">Projects</Link>
        <span>/</span>
        <Link to={`/projects/${id}`}>{project?.name}</Link>
        <span>/</span>
        <span>{doc.filename}</span>
      </div>

      <div className="doc-head">
        <div className="doc-title-block">
          <h1 className="doc-name">{doc.filename}</h1>
          <p className="muted small">{doc.content_type}</p>
        </div>
        <div className="doc-actions">
          {kind === 'markdown' && text !== null && (
            <div className="segmented">
              <button className={!rawMarkdown ? 'active' : ''} onClick={() => setRawMarkdown(false)}>Rendered</button>
              <button className={rawMarkdown ? 'active' : ''} onClick={() => setRawMarkdown(true)}>Source</button>
            </div>
          )}
          <button className="btn btn-primary" onClick={download}>Download</button>
          <button className="btn danger" onClick={remove}>Delete</button>
        </div>
      </div>

      {error && <p className="error" style={{ marginTop: 12 }}>{error}</p>}

      <div className="preview">
        {!kind && (
          <div className="no-preview">
            <h3>No preview for this file type</h3>
            <p className="muted">Download {doc.filename} to open it on your device.</p>
            <button className="btn btn-primary" onClick={download}>Download</button>
          </div>
        )}
        {kind && loading && <p className="center-note">Loading preview…</p>}
        {kind === 'image' && url && <img src={url} alt={doc.filename} className="preview-image" />}
        {kind === 'pdf' && url && <iframe src={url} title={doc.filename} className="preview-frame" />}
        {kind === 'video' && url && <video src={url} controls className="preview-media" />}
        {kind === 'audio' && url && <audio src={url} controls className="preview-audio" />}
        {kind === 'text' && text !== null && <pre className="preview-text">{text || 'This file is empty.'}</pre>}
        {kind === 'markdown' && text !== null &&
          (rawMarkdown ? (
            <pre className="preview-text">{text}</pre>
          ) : (
            <article className="prose" dangerouslySetInnerHTML={{ __html: renderMarkdown(text) || '<p class="muted">This file is empty.</p>' }} />
          ))}
        {truncated && <p className="muted small preview-note">Showing the first 1,000,000 characters. Download the file to see everything.</p>}
      </div>
    </div>
  );
}
