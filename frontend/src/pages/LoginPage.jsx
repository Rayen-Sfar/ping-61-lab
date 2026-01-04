 
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import API from '../services/api';

export default function LoginPage() {
  const navigate = useNavigate();
  const { setUser, setToken } = useAuth();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // ✅ Étape 1 : Vérifier si un ticket CAS est présent dans l'URL
    const urlParams = new URLSearchParams(window.location.search);
    const casTicket = urlParams.get('ticket');

    if (casTicket) {
      // ✅ Étape 2 : Envoyer le ticket au backend pour validation
      handleCasCallback(casTicket);
    } else {
      // ✅ Première visite : rediriger vers CAS
      redirectToCAS();
    }
  }, []);

  const redirectToCAS = async () => {
    try {
      const response = await API.get('/auth/login');
      const { redirect_url } = response.data;
      
      // Rediriger vers le serveur CAS
      window.location.href = redirect_url;
    } catch (err) {
      setError('Impossible de se connecter à CAS');
      setLoading(false);
    }
  };

  const handleCasCallback = async (ticket) => {
    try {
      // Appeler le backend avec le ticket
      const response = await API.get('/auth/callback', {
        params: { ticket }
      });

      const { access_token, user_id, role } = response.data;

      // ✅ Stocker JWT + infos utilisateur
      localStorage.setItem('token', access_token);
      localStorage.setItem('user_id', user_id);
      localStorage.setItem('role', role);

      // Mettre à jour contexte
      setToken(access_token);
      setUser({ id: user_id, role });

      // ✅ Rediriger au dashboard
      setTimeout(() => {
        navigate('/dashboard');
      }, 1000);
    } catch (err) {
      setError(`❌ Erreur CAS : ${err.response?.data?.detail || 'Erreur inconnue'}`);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <div>
          <h2>🔐 Authentification en cours...</h2>
          <p>Redirection vers le serveur CAS</p>
        </div>
      </div>
    );
  }

  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      {error && (
        <div style={{ color: 'red', fontSize: '18px', marginBottom: '20px' }}>
          {error}
        </div>
      )}
      <button onClick={redirectToCAS}>
        Réessayer la connexion
      </button>
    </div>
  );
}