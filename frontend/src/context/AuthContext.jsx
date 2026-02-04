import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export const useAuth = () => {
  return useContext(AuthContext);
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);

  useEffect(() => {
    const storedToken = localStorage.getItem('token');
    const storedUserId = localStorage.getItem('user_id');
    const storedRole = localStorage.getItem('role');
    const storedUsername = localStorage.getItem('username');

    if (storedToken && storedUserId) {
      setToken(storedToken);
      setUser({ id: storedUserId, role: storedRole, username: storedUsername });
    }
  }, []);

  const logout = () => {
    // Clean up local storage and auth state
    localStorage.removeItem('token');
    localStorage.removeItem('user_id');
    localStorage.removeItem('role');
    localStorage.removeItem('username');
    setToken(null);
    setUser(null);

    // Redirect to the public landing/login page
    // Explicitly use the host:port requested (http://localhost:3000)
    try {
      window.location.href = 'http://localhost:3000';
    } catch (err) {
      // Fallback: navigate to root of SPA
      window.location.assign('/');
    }
  };

  return (
    <AuthContext.Provider value={{ user, token, setUser, setToken, logout }}>
      {children}
    </AuthContext.Provider>
  );
};