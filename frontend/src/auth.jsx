import { createContext, useContext, useEffect, useState } from 'react';
import { api } from './api.js';

const Ctx = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(!!localStorage.getItem('token'));

  useEffect(() => {
    if (!localStorage.getItem('token')) return;
    api('/auth/me/')
      .then(setUser)
      .catch(() => localStorage.removeItem('token'))
      .finally(() => setLoading(false));
  }, []);

  // POST /token expects OAuth2 form data: username + password
  const login = async (username, password) => {
    const d = await api('/token', { method: 'POST', body: new URLSearchParams({ username, password }) });
    localStorage.setItem('token', d.access_token);
    setUser(d.user);
    return d.user;
  };

  // POST /auth creates the user, then we sign in right away
  const register = async ({ username, email, password, repeat_password }) => {
    await api('/auth', {
      method: 'POST',
      body: { username, email: email || null, password, repeat_password },
    });
    return login(username, password);
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  return <Ctx.Provider value={{ user, loading, login, register, logout }}>{children}</Ctx.Provider>;
}

export const useAuth = () => useContext(Ctx);
