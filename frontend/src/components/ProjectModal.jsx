import { useState } from 'react';
import { api } from '../api.js';
import { normalizeProject } from '../utils.js';
import Modal from './Modal.jsx';

export default function ProjectModal({ project, onClose, onSaved }) {
  const [name, setName] = useState(project?.name || '');
  const [description, setDescription] = useState(project?.description || '');
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);

  async function submit(e) {
    e.preventDefault();
    setBusy(true);
    setError('');
    try {
      const d = project
        ? await api(`/project/${project.id}/info`, { method: 'PUT', body: { name, description } })
        : await api('/projects', { method: 'POST', body: { name, description } });
      // only owners can reach this modal, so the saved project is always theirs
      onSaved({ ...normalizeProject(d), is_owner: true });
    } catch (err) {
      setError(err.message);
      setBusy(false);
    }
  }

  return (
    <Modal title={project ? 'Edit project' : 'New project'} onClose={onClose}>
      <form onSubmit={submit} className="stack">
        <label className="field">
          <span>Name</span>
          <input value={name} onChange={(e) => setName(e.target.value)} maxLength={80} autoFocus required />
        </label>
        <label className="field">
          <span>Description</span>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            maxLength={400}
            rows={3}
            placeholder="What is this project about?"
          />
        </label>
        {error && <p className="error">{error}</p>}
        <div className="modal-actions">
          <button type="button" className="btn btn-ghost" onClick={onClose}>Cancel</button>
          <button className="btn btn-primary" disabled={busy}>{project ? 'Save changes' : 'Create project'}</button>
        </div>
      </form>
    </Modal>
  );
}
