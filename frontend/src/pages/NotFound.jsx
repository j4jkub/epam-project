import { Link } from 'react-router-dom';

export default function NotFound() {
  return (
    <div className="container section">
      <div className="empty">
        <h3>Page not found</h3>
        <p className="muted">The page you’re looking for doesn’t exist or was moved.</p>
        <Link to="/" className="btn">Go home</Link>
      </div>
    </div>
  );
}
