// Only routed when FEATURES.emailInvite is true (see src/config.js)
import { useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { api } from '../api.js';
import { useAuth } from '../auth.jsx';

export default function AcceptInvite() {
  const { token } = useParams();
  const { user, loading } = useAuth();
  const navigate = useNavigate();
  const [invite, setInvite] = useState(null);
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  const here = `/invite/${token}`;

  useEffect(() => {
    api(`/invites/${token}`).then(setInvite).catch((e) => setError(e.message));
  }, [token]);

  async function accept() {
    setBusy(true);
    try {
      const d = await api(`/invites/${token}/accept`, { method: 'POST' });
      navigate(`/projects/${d.project_id}`, { replace: true });
    } catch (e) {
      setError(e.message);
      setBusy(false);
    }
  }

  return (
    <div className="auth">
      <div className="auth-card stack">
        {error ? (
          <>
            <h2>Invite unavailable</h2>
            <p className="error">{error}</p>
            <Link className="btn btn-block" to="/projects">Go to projects</Link>
          </>
        ) : !invite || loading ? (
          <p className="muted">Checking invite…</p>
        ) : (
          <>
            <h2>Join “{invite.project_name}”</h2>
            <p className="muted">{invite.invited_by} invited you to collaborate.</p>
            {user ? (
              <button className="btn btn-primary btn-block" onClick={accept} disabled={busy}>
                Join as {user.username}
              </button>
            ) : (
              <>
                <Link className="btn btn-primary btn-block" to="/register" state={{ from: here }}>Create an account to join</Link>
                <Link className="btn btn-block" to="/login" state={{ from: here }}>I already have an account</Link>
              </>
            )}
          </>
        )}
      </div>
    </div>
  );
}
