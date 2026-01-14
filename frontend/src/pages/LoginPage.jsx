 
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function LoginPage() {
  const navigate = useNavigate();
  const { setUser, setToken } = useAuth();
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Pour les tests : connexion automatique avec un utilisateur mock
    handleMockLogin();
  }, []);

  const handleMockLogin = () => {
    setLoading(true);
    
    // Simuler un utilisateur connecté
    const mockToken = "mock-jwt-token";
    const mockUser = { id: "1", role: "student" };
    
    // Stocker dans localStorage
    localStorage.setItem('token', mockToken);
    localStorage.setItem('user_id', mockUser.id);
    localStorage.setItem('role', mockUser.role);
    
    // Mettre à jour contexte
    setToken(mockToken);
    setUser(mockUser);
    
    // Rediriger vers dashboard
    setTimeout(() => {
      navigate('/dashboard');
    }, 1000);
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', flexDirection: 'column' }}>
      <h1>Lab on Demand</h1>
      {loading ? (
        <div>
          <h2>🔐 Connexion automatique en cours...</h2>
          <p>Redirection vers le dashboard</p>
        </div>
      ) : (
        <button onClick={handleMockLogin}>
          Connexion Test (Mock)
        </button>
      )}
    </div>
  );
}