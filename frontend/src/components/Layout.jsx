import { Link, NavLink, Outlet, useNavigate } from 'react-router-dom';
import { useAuth } from '../auth.jsx';
import Avatar from './Avatar.jsx';

export function Logo() {
  return (
    <Link to="/" className="logo">
      <svg width="22" height="22" viewBox="0 0 32 32" aria-hidden="true">
        <rect width="32" height="32" rx="8" fill="currentColor" />
        <path d="M9 9h6v14H9zM17 9h6v8h-6z" fill="var(--bg)" />
      </svg>
      Ledgerly
    </Link>
  );
}

function Header() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  return (
    <header className="header">
      <div className="container header-inner">
        <Logo />
        <nav className="nav">
          {user ? (
            <>
              <NavLink to="/projects">Projects</NavLink>
              <NavLink to="/profile" className="nav-user">
                <Avatar name={user.username} size={22} />
                {user.username}
              </NavLink>
              <button
                className="btn btn-ghost btn-sm"
                onClick={() => {
                  logout();
                  navigate('/');
                }}
              >
                Log out
              </button>
            </>
          ) : (
            <>
              <NavLink to="/login">Log in</NavLink>
              <Link to="/register" className="btn btn-primary btn-sm">Create account</Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
}

function Footer() {
  const { user } = useAuth();
  return (
    <footer className="footer">
      <div className="container footer-inner">
        <div>
          <Logo />
          <p className="muted small">Projects, documents and the people behind them.</p>
        </div>
        <div className="footer-links">
          {user ? (
            <>
              <Link to="/projects">Projects</Link>
              <Link to="/profile">Profile</Link>
            </>
          ) : (
            <>
              <Link to="/login">Log in</Link>
              <Link to="/register">Create account</Link>
            </>
          )}
        </div>
        <p className="muted small footer-copy">© {new Date().getFullYear()} Ledgerly</p>
      </div>
    </footer>
  );
}

export default function Layout() {
  return (
    <div className="shell">
      <Header />
      <main className="main">
        <Outlet />
      </main>
      <Footer />
    </div>
  );
}
