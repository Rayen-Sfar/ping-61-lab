import React, { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import API from '../services/api';
import '../styles/LoginPage.css';

export default function LoginPage() {
  const navigate = useNavigate();
  const { user, setUser, setToken } = useAuth();
  const [searchParams] = useSearchParams();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Si l'utilisateur est déjà connecté, rediriger selon son rôle
  // MAIS si un ticket CAS est présent, laisser le handler du ticket décider de la redirection
  const ticketParam = searchParams.get('ticket');
  useEffect(() => {
    if (!user) return;
    if (ticketParam) return; // Eviter d'interrompre le flux CAS en cours

    const role = (user.role || '').toString().toLowerCase();
    if (role === 'teacher' || role === 'admin') {
      navigate('/admin');
    } else {
      navigate('/dashboard');
    }
  }, [user, navigate, ticketParam]);

  // Persist redirect target (if any) so it survives CAS external redirect
  const redirectParam = searchParams.get('redirect');
  if (redirectParam) {
    sessionStorage.setItem('redirect_after_login', redirectParam);
  }

  useEffect(() => {
    // Vérifier si on revient de CAS avec un ticket
    const ticket = searchParams.get('ticket');
    if (ticket) {
      handleCASCallback(ticket);
    }
  }, [searchParams]);

  const handleCASCallback = async (ticket) => {
    // Éviter de traiter le même ticket plusieurs fois (React StrictMode peut double-invoquer)
    if (sessionStorage.getItem(`ticket_${ticket}`)) {
      console.warn('Ticket déjà traité:', ticket);
      return;
    }
    sessionStorage.setItem(`ticket_${ticket}`, '1');

    setLoading(true);
    setError('');
    
    try {
      // Ne pas lever d'exception sur redirect 3xx ici - nous allons vérifier le contenu
      const response = await API.get(`/auth/callback?ticket=${ticket}`, { validateStatus: null });

      // Vérifier que le backend a retourné un access_token valide
      if (response.status !== 200 || !response.data || !response.data.access_token) {
        console.error('CAS callback failed:', response.status, response.data);
        setError('Échec de l\'authentification CAS (ticket invalide ou expiré). Veuillez réessayer.');
        setLoading(false);
        return;
      }

      const { access_token, user_id, username, role } = response.data;

      // Sécurité : ne pas stocker des valeurs indéfinies
      if (!access_token) {
        setError('Échec de l\'authentification CAS. Jeton manquant.');
        setLoading(false);
        return;
      }

      // Stocker dans localStorage
      localStorage.setItem('token', access_token);
      localStorage.setItem('user_id', user_id);
      localStorage.setItem('role', role);
      localStorage.setItem('username', username);
      
      // Mettre à jour contexte
      setToken(access_token);
      setUser({ id: user_id, role, username });
      
      // Rediriger selon le redirect stocké (si présent) ou selon le rôle
      const redirectAfterLogin = sessionStorage.getItem('redirect_after_login');
      if (redirectAfterLogin) {
        sessionStorage.removeItem('redirect_after_login');
        navigate(redirectAfterLogin);
      } else if (role === 'teacher' || role === 'admin') {
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
      const response = await API.get('/auth/login');
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