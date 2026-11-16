import { Link, Navigate } from 'react-router-dom';
import { useAuth } from '../auth.jsx';

export default function Home() {
  const { user, loading } = useAuth();
  if (!loading && user) return <Navigate to="/projects" replace />;

  return (
    <>
      <section className="hero">
        <div className="container">
          <h1>Keep the work and the people in one quiet place.</h1>
          <p>
            Create a project, drop in the files that matter, and add your team by username.
          </p>
          <div className="hero-actions">
            <Link to="/register" className="btn btn-primary btn-lg">Start a project</Link>
            <Link to="/login" className="btn btn-lg">Log in</Link>
          </div>
        </div>
      </section>

      <section className="container features">
        <div>
          <h3>Projects you own</h3>
          <p>Create, rename and remove your own projects. Nobody else can change what you built.</p>
        </div>
        <div>
          <h3>Any file, previewed</h3>
          <p>Upload documents of any type. Images, PDFs, text, audio and video open right in the browser.</p>
        </div>
        <div>
          <h3>Bring your team</h3>
          <p>Add a teammate by username and they can see and upload to the project straight away.</p>
        </div>
      </section>
    </>
  );
}
