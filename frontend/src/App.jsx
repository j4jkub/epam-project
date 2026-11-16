import { Navigate, Route, Routes, useLocation } from 'react-router-dom';
import { useAuth } from './auth.jsx';
import { FEATURES } from './config.js';
import Layout from './components/Layout.jsx';
import Home from './pages/Home.jsx';
import Login from './pages/Login.jsx';
import Register from './pages/Register.jsx';
import Projects from './pages/Projects.jsx';
import Project from './pages/Project.jsx';
import Document from './pages/Document.jsx';
import Profile from './pages/Profile.jsx';
import AcceptInvite from './pages/AcceptInvite.jsx';
import NotFound from './pages/NotFound.jsx';

function RequireAuth({ children }) {
  const { user, loading } = useAuth();
  const location = useLocation();
  if (loading) return <div className="center-note">Loading…</div>;
  if (!user) return <Navigate to="/login" replace state={{ from: location.pathname }} />;
  return children;
}

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="login" element={<Login />} />
        <Route path="register" element={<Register />} />
        {FEATURES.emailInvite && <Route path="invite/:token" element={<AcceptInvite />} />}
        <Route path="projects" element={<RequireAuth><Projects /></RequireAuth>} />
        <Route path="projects/:id" element={<RequireAuth><Project /></RequireAuth>} />
        <Route path="projects/:id/docs/:docId" element={<RequireAuth><Document /></RequireAuth>} />
        <Route path="profile" element={<RequireAuth><Profile /></RequireAuth>} />
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}
