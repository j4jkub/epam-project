import { useState } from 'react';
import { Link, Navigate, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../auth.jsx';

export default function Register() {
  const { user, register } = useAuth();
  const navigate = useNavigate();
  const from = useLocation().state?.from || '/projects';
  const [form, setForm] = useState({ username: '', email: '', password: '', repeat_password: '' });
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  const set = (k) => (e) => setForm({ ...form, [k]: e.target.value });

  if (user) return <Navigate to={from} replace />;

  async function submit(e) {
    e.preventDefault();
    if (form.password !== form.repeat_password) return setError('Passwords don’t match');
    setBusy(true);
    setError('');
    try {
      await register(form);
      navigate(from, { replace: true });
    } catch (err) {
      setError(err.message);
      setBusy(false);
    }
  }

  return (
    <div className="auth">
      <form className="auth-card stack" onSubmit={submit}>
        <h2>Create your account</h2>
        <p className="muted">It takes a few seconds.</p>
        <label className="field">
          <span>Username</span>
          <input value={form.username} onChange={set('username')} autoFocus required placeholder="e.g. ada_l" />
        </label>
        <label className="field">
          <span>Email <small className="muted">(optional)</small></span>
          <input type="email" value={form.email} onChange={set('email')} />
        </label>
        <label className="field">
          <span>Password</span>
          <input type="password" value={form.password} onChange={set('password')} required />
        </label>
        <label className="field">
          <span>Repeat password</span>
          <input type="password" value={form.repeat_password} onChange={set('repeat_password')} required />
        </label>
        {error && <p className="error">{error}</p>}
        <button className="btn btn-primary btn-block" disabled={busy}>Create account</button>
        <p className="muted small center">
          Already registered? <Link to="/login" state={{ from }}>Log in</Link>
        </p>
      </form>
    </div>
  );
}
