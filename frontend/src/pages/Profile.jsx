import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../api.js';
import { useAuth } from '../auth.jsx';
import Avatar from '../components/Avatar.jsx';
import Banner from '../components/Banner.jsx';

export default function Profile() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);

  useEffect(() => {
    api('/projects').then((list) =>
      setStats({
        owned: list.filter((p) => p.is_owner).length,
        shared: list.filter((p) => !p.is_owner).length,
      })
    );
  }, []);

  return (
    <>
      <Banner title={user.username} subtitle={`Account #${user.id}`}>
        <Avatar name={user.username} size={56} />
      </Banner>

      <div className="container section">
        <div className="stats">
          <div><strong>{stats?.owned ?? '–'}</strong><span>projects owned</span></div>
          <div><strong>{stats?.shared ?? '–'}</strong><span>shared with you</span></div>
        </div>

        <div className="card stack" style={{ maxWidth: 420 }}>
          <h3>Account</h3>
          <div className="field">
            <span>Username</span>
            <p>{user.username}</p>
          </div>
          <button
            className="btn"
            onClick={() => {
              logout();
              navigate('/');
            }}
          >
            Log out
          </button>
        </div>
      </div>
    </>
  );
}
