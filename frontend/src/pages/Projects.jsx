import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../api.js';
import { useAuth } from '../auth.jsx';
import Banner from '../components/Banner.jsx';
import ProjectModal from '../components/ProjectModal.jsx';
import Avatar from '../components/Avatar.jsx';
import { normalizeProject } from '../utils.js';

export default function Projects() {
  const { user } = useAuth();
  const [projects, setProjects] = useState(null);
  const [filter, setFilter] = useState('all');
  const [modal, setModal] = useState(null); // { project? }
  const [error, setError] = useState('');

  useEffect(() => {
    api('/projects')
      .then((list) => setProjects(list.map(normalizeProject).sort((a, b) => b.id - a.id)))
      .catch((e) => setError(e.message));
  }, []);

  async function remove(p) {
    if (!confirm(`Delete “${p.name}” and all of its documents? This can't be undone.`)) return;
    try {
      await api(`/project/${p.id}`, { method: 'DELETE' });
      setProjects((list) => list.filter((x) => x.id !== p.id));
    } catch (e) {
      setError(e.message);
    }
  }

  const onSaved = (p) => {
    setProjects((list) => {
      const exists = list.some((x) => x.id === p.id);
      return exists ? list.map((x) => (x.id === p.id ? p : x)) : [p, ...list];
    });
    setModal(null);
  };

  const shown = (projects || []).filter(
    (p) => filter === 'all' || (filter === 'owned' ? p.is_owner : !p.is_owner)
  );

  return (
    <>
      <Banner title="Projects" subtitle={`Hi ${user.username}. Pick up where you left off or start something new.`}>
        <button className="btn btn-primary" onClick={() => setModal({})}>New project</button>
      </Banner>

      <div className="container section">
        <div className="toolbar">
          <div className="tabs">
            {[['all', 'All'], ['owned', 'Owned by me'], ['shared', 'Shared with me']].map(([k, label]) => (
              <button key={k} className={filter === k ? 'tab active' : 'tab'} onClick={() => setFilter(k)}>
                {label}
              </button>
            ))}
          </div>
          {projects && <span className="muted small">{shown.length} {shown.length === 1 ? 'project' : 'projects'}</span>}
        </div>

        {error && <p className="error">{error}</p>}
        {!projects && !error && <p className="muted">Loading projects…</p>}

        {projects && shown.length === 0 && (
          <div className="empty">
            <h3>{filter === 'shared' ? 'Nothing shared with you yet' : 'No projects yet'}</h3>
            <p className="muted">
              {filter === 'shared'
                ? 'When someone adds you to their project, it will show up here.'
                : 'Create your first project to start uploading files and adding people.'}
            </p>
            {filter !== 'shared' && <button className="btn btn-primary" onClick={() => setModal({})}>New project</button>}
          </div>
        )}

        <div className="grid">
          {shown.map((p) => (
            <article key={p.id} className="card project-card">
              <Link to={`/projects/${p.id}`} className="card-link">
                <div className="card-top">
                  <h3>{p.name}</h3>
                  <span className={`badge ${p.is_owner ? 'owner' : ''}`}>{p.is_owner ? 'Owner' : 'Member'}</span>
                </div>
                <p className="muted clamp">{p.description || 'No description'}</p>
              </Link>
              <div className="card-foot">
                <div className="avatars">
                  {p.owner && <Avatar name={p.owner.username} size={24} />}
                  {p.participants.slice(0, 3).map((m) => <Avatar key={m.id} name={m.username} size={24} />)}
                  {p.participants.length > 3 && <span className="muted small">+{p.participants.length - 3}</span>}
                </div>
                <span className="muted small">
                  {p.participants.length + 1} {p.participants.length ? 'people' : 'person'}
                </span>
              </div>
              {p.is_owner && (
                <div className="card-actions">
                  <button className="btn btn-ghost btn-sm" onClick={() => setModal({ project: p })}>Edit</button>
                  <button className="btn btn-ghost btn-sm danger" onClick={() => remove(p)}>Delete</button>
                </div>
              )}
            </article>
          ))}
        </div>
      </div>

      {modal && <ProjectModal project={modal.project} onClose={() => setModal(null)} onSaved={onSaved} />}
    </>
  );
}
