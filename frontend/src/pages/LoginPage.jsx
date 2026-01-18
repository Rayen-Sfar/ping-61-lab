import React, { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import API from '../services/api';
import '../styles/LoginPage.css';

export default function LoginPage() {
  const navigate = useNavigate();
  const { setUser, setToken } = useAuth();
  const [searchParams] = useSearchParams();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    // Vérifier si on revient de CAS avec un ticket
    const ticket = searchParams.get('ticket');
    if (ticket) {
      handleCASCallback(ticket);
    }
  }, [searchParams]);

  const handleCASCallback = async (ticket) => {
    setLoading(true);
    setError('');
    
    try {
      const response = await API.get(`/api/auth/callback?ticket=${ticket}`);
      const { access_token, user_id, username, role } = response.data;
      
      // Stocker dans localStorage
      localStorage.setItem('token', access_token);
      localStorage.setItem('user_id', user_id);
      localStorage.setItem('role', role);
      localStorage.setItem('username', username);
      
      // Mettre à jour contexte
      setToken(access_token);
      setUser({ id: user_id, role, username });
      
      // Rediriger selon le rôle
      if (role === 'teacher' || role === 'admin') {
        navigate('/admin');
      } else {
        navigate('/dashboard');
      }
    } catch (err) {
      console.error('Erreur CAS:', err);
      setError('Échec de l\'authentification CAS. Veuillez réessayer.');
      setLoading(false);
    }
  };

  const handleCASLogin = async () => {
    setLoading(true);
    setError('');
    
    try {
      // Récupérer l'URL de redirection CAS
      const response = await API.get('/api/auth/login');
      const { redirect_url } = response.data;
      
      // Rediriger vers CAS
      window.location.href = redirect_url;
    } catch (err) {
      console.error('Erreur lors de la redirection CAS:', err);
      setError('Impossible de se connecter au serveur CAS.');
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-content">
        <div className="login-form-wrapper">
          {/* Logo et titre */}
          <div className="login-header">
            <div className="logo-box">
              <svg className="logo-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="10" fill="currentColor" opacity="0.2"/>
                <text x="12" y="15" textAnchor="middle" fontSize="20" fontWeight="bold" fill="currentColor">
                  ©
                </text>
              </svg>
              <span className="logo-text">esigelec</span>
            </div>
            <h1 className="login-title">Lab on Demand</h1>
            <p className="login-subtitle">Plateforme de Travaux Pratiques</p>
          </div>

          {/* Message d'erreur */}
          {error && (
            <div className="alert alert-error">
              {error}
            </div>
          )}

          {/* Bouton de connexion CAS */}
          <div className="cas-login-section">
            <p className="cas-info">
              🔐 Connectez-vous avec vos identifiants ESIGELEC
            </p>
            
            <button
              onClick={handleCASLogin}
              className="btn-cas-login"
              disabled={loading}
            >
              {loading ? (
                <span>⏳ Redirection en cours...</span>
              ) : (
                <span>🎓 SE CONNECTER VIA CAS</span>
              )}
            </button>

            <div className="cas-help">
              <p>Comptes de test :</p>
              <ul>
                <li>Étudiant : student1 / password123</li>
                <li>Enseignant : teacher1 / password123</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* Background image */}
      <div className="login-background"></div>
    </div>
  );
}