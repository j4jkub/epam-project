import { useEffect, useRef, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { api } from '../api.js';
import { useAuth } from '../auth.jsx';
import { FEATURES } from '../config.js';
import { downloadDocument, previewKind } from '../files.js';
import { normalizeProject } from '../utils.js';
import Banner from '../components/Banner.jsx';
import Avatar from '../components/Avatar.jsx';
import FileBadge from '../components/FileBadge.jsx';
import ProjectModal from '../components/ProjectModal.jsx';

export default function Project() {
  const { id } = useParams();
  const { user } = useAuth();
  const navigate = useNavigate();
  const [project, setProject] = useState(null);
  const [docs, setDocs] = useState(null);
  const [error, setError] = useState('');
  const [actionError, setActionError] = useState('');
  const [editing, setEditing] = useState(false);
  const [uploading, setUploading] = useState(null);
  const [dragging, setDragging] = useState(false);
  const fileInput = useRef(null);

  const reload = async () => setProject(normalizeProject(await api(`/project/${id}/info`)));

  useEffect(() => {
    Promise.all([api(`/project/${id}/info`), api(`/project/${id}/documents`)])
      .then(([p, d]) => {
        setProject(normalizeProject(p));
        setDocs([...d].sort((a, b) => b.id - a.id));
      })
      .catch((e) => setError(e.message));
  }, [id]);

  if (error) {
    return (
      <div className="container section">
        <div className="empty">
          <h3>{error}</h3>
          <Link to="/projects" className="btn">Back to projects</Link>
        </div>
      </div>
    );
  }
  if (!project) return <div className="center-note">Loading…</div>;

  const isOwner = project.is_owner;

  async function deleteProject() {
    if (!confirm(`Delete “${project.name}” and all of its documents? This can't be undone.`)) return;
    try {
      await api(`/project/${id}`, { method: 'DELETE' });
      navigate('/projects');
    } catch (e) {
      setActionError(e.message);
    }
  }

  async function leave() {
    if (!confirm(`Leave “${project.name}”?`)) return;
    try {
      await api(`/project/${id}/invite?user=${encodeURIComponent(user.username)}`, { method: 'DELETE' });
      navigate('/projects');
    } catch (e) {
      setActionError(e.message);
    }
  }

  async function upload(files) {
    setActionError('');
    for (const file of files) {
      setUploading(file.name);
      try {
        const body = new FormData();
        body.append('file', file);
        const doc = await api(`/project/${id}/documents`, { method: 'POST', body });
        setDocs((list) => [doc, ...(list || [])]);
      } catch (e) {
        setActionError(`${file.name}: ${e.message}`);
      }
    }
    setUploading(null);
  }

  async function removeDoc(d) {
    if (!confirm(`Delete “${d.filename}”? This can't be undone.`)) return;
    try {
      await api(`/document/${d.id}`, { method: 'DELETE' });
      setDocs((list) => list.filter((x) => x.id !== d.id));
    } catch (e) {
      setActionError(e.message);
    }
  }

  async function download(d) {
    try {
      await downloadDocument(d);
    } catch (e) {
      setActionError(e.message);
    }
  }

  return (
    <>
      <Banner
        title={project.name}
        subtitle={project.description}
        meta={
          <>
            <Link to="/projects">Projects</Link>
            <span>/</span>
            <span>{isOwner ? 'Owned by you' : `Owned by ${project.owner?.username ?? 'unknown'}`}</span>
          </>
        }
      >
        {isOwner ? (
          <>
            <button className="btn" onClick={() => setEditing(true)}>Edit</button>
            <button className="btn danger" onClick={deleteProject}>Delete</button>
          </>
        ) : (
          <button className="btn" onClick={leave}>Leave project</button>
        )}
      </Banner>

      <div className="container section project-layout">
        <section
          className={dragging ? 'drop-target dragging' : 'drop-target'}
          onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
          onDragLeave={() => setDragging(false)}
          onDrop={(e) => {
            e.preventDefault();
            setDragging(false);
            upload([...e.dataTransfer.files]);
          }}
        >
          <div className="section-head">
            <h2>Documents</h2>
            <button className="btn btn-primary btn-sm" onClick={() => fileInput.current.click()} disabled={!!uploading}>
              {uploading ? 'Uploading…' : 'Upload files'}
            </button>
            <input
              ref={fileInput}
              type="file"
              multiple
              hidden
              onChange={(e) => {
                upload([...e.target.files]);
                e.target.value = '';
              }}
            />
          </div>

          {actionError && <p className="error" style={{ marginBottom: 12 }}>{actionError}</p>}
          {uploading && <p className="muted small" style={{ marginBottom: 12 }}>Uploading {uploading}…</p>}
          {!docs && <p className="muted">Loading documents…</p>}

          {docs && docs.length === 0 && (
            <div className="empty">
              <h3>No documents yet</h3>
              <p className="muted">Drop files here or upload them. Any file type works.</p>
              <button className="btn btn-primary" onClick={() => fileInput.current.click()}>Upload files</button>
            </div>
          )}

          <div className="doc-list">
            {docs?.map((d) => (
              <div key={d.id} className="doc-row">
                <Link to={`/projects/${id}/docs/${d.id}`} className="doc-main">
                  <FileBadge filename={d.filename} />
                  <div>
                    <h4>{d.filename}</h4>
                    <p className="muted small">{d.content_type}</p>
                  </div>
                </Link>
                <div className="row-actions">
                  {previewKind(d) && (
                    <Link to={`/projects/${id}/docs/${d.id}`} className="btn btn-ghost btn-sm">Preview</Link>
                  )}
                  <button className="btn btn-ghost btn-sm" onClick={() => download(d)}>Download</button>
                  <button className="btn btn-ghost btn-sm danger" onClick={() => removeDoc(d)}>Delete</button>
                </div>
              </div>
            ))}
          </div>
        </section>

        <aside>
          <Members project={project} isOwner={isOwner} reload={reload} />
        </aside>
      </div>

      {editing && (
        <ProjectModal
          project={project}
          onClose={() => setEditing(false)}
          onSaved={(p) => {
            setProject(p);
            setEditing(false);
          }}
        />
      )}
    </>
  );
}

function Members({ project, isOwner, reload }) {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const [notice, setNotice] = useState(null); // { text, link }
  const [busy, setBusy] = useState(false);

  async function addByUsername(e) {
    e.preventDefault();
    setError('');
    setNotice(null);
    try {
      await api(`/project/${project.id}/invite?user=${encodeURIComponent(username)}`, { method: 'POST' });
      await reload();
      setNotice({ text: `${username} was added to the project.` });
      setUsername('');
    } catch (err) {
      setError(err.message);
    }
  }

  async function inviteByEmail(e) {
    e.preventDefault();
    setError('');
    setNotice(null);
    setBusy(true);
    try {
      const d = await api(`/project/${project.id}/invite/email?email=${encodeURIComponent(email)}`, { method: 'POST' });
      setNotice({
        text: d?.sent ? `Invitation sent to ${email}.` : 'Email wasn’t sent. Share this link with them directly:',
        link: d?.sent ? null : d?.link,
      });
      setEmail('');
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  async function removeMember(m) {
    if (!confirm(`Remove ${m.username} from this project?`)) return;
    try {
      await api(`/project/${project.id}/invite?user=${encodeURIComponent(m.username)}`, { method: 'DELETE' });
      await reload();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div className="card side-card">
      <h3>People</h3>
      <ul className="people">
        {project.owner && (
          <li>
            <Avatar name={project.owner.username} />
            <span>{project.owner.username}</span>
            <span className="badge owner">Owner</span>
          </li>
        )}
        {project.participants.map((m) => (
          <li key={m.id}>
            <Avatar name={m.username} />
            <span>{m.username}</span>
            {isOwner && (
              <button className="icon-btn" title={`Remove ${m.username}`} onClick={() => removeMember(m)}>✕</button>
            )}
          </li>
        ))}
      </ul>

      {isOwner && (
        <div className="stack invite-forms">
          <form onSubmit={addByUsername} className="inline-form">
            <input placeholder="Add by username" value={username} onChange={(e) => setUsername(e.target.value)} required />
            <button className="btn btn-sm">Add</button>
          </form>
          {FEATURES.emailInvite && (
            <form onSubmit={inviteByEmail} className="inline-form">
              <input type="email" placeholder="Invite by email" value={email} onChange={(e) => setEmail(e.target.value)} required />
              <button className="btn btn-sm" disabled={busy}>Send</button>
            </form>
          )}
          {error && <p className="error small">{error}</p>}
          {notice && (
            <div className="notice small">
              <p>{notice.text}</p>
              {notice.link && (
                <div className="copy-row">
                  <input readOnly value={notice.link} onFocus={(e) => e.target.select()} />
                  <button className="btn btn-sm" onClick={() => navigator.clipboard?.writeText(notice.link)}>Copy</button>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
