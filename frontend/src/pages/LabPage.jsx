import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import { useAuth } from '../context/AuthContext';
import API from '../services/api';

const GUAC_BASE = process.env.REACT_APP_GUAC_BASE || 'http://localhost:8088/guacamole';

const LabPage = () => {
  const { tpId } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [tp, setTp] = useState(null);
  const [guacamoleUrl, setGuacamoleUrl] = useState('');
  const [timer, setTimer] = useState(0);
  const [showInstructions, setShowInstructions] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Vérifier si l'utilisateur est authentifié
    const token = localStorage.getItem('token');
    console.log('🔍 Token dans localStorage:', token ? '✅ Présent' : '❌ Absent');
    console.log('👤 User contexte:', user);
    
    if (!token || !user) {
      console.log('❌ Pas de token ou user, redirection vers login');
      navigate('/');
      return;
    }
    
    fetchTPAndGuacamoleAccess();
    const interval = setInterval(() => setTimer(t => t + 1), 1000);
    return () => clearInterval(interval);
  }, [tpId, user, navigate]);

  const fetchTPAndGuacamoleAccess = async () => {
    try {
      setLoading(true);
      setError(null);

      const token = localStorage.getItem('token');
      console.log('📤 Token envoyé dans requête:', token ? `${token.substring(0, 20)}...` : 'VIDE');

      // 1️⃣ Récupérer les détails du TP
      const tpResponse = await API.get(`/tp/${tpId}`);
      setTp(tpResponse.data);

      // 2️⃣ Obtenir l'accès direct à Guacamole avec authentification CAS
      // ✅ Accès automatique - pas besoin de login supplémentaire
      const guacResponse = await API.get(`/tp/${tpId}/guacamole-access`);
      
      if (guacResponse.data.guacamole_url) {
        setGuacamoleUrl(guacResponse.data.guacamole_url);
        console.log(`✅ Accès Guacamole direct pour: ${guacResponse.data.username}`);
        console.log(`� URL Guacamole retournée par backend: ${guacResponse.data.guacamole_url}`);
        console.log(`�🖥️ Machine: ${guacResponse.data.vm_name} (ID: ${guacResponse.data.vm_id})`);
      } else {
        setError('Impossible de générer l\'accès Guacamole');
      }
    } catch (error) {
      console.error('❌ Erreur lors de l\'accès au TP:', error);
      console.error('📍 Status:', error.response?.status);
      console.error('📝 Detail:', error.response?.data?.detail);
      setError(error.response?.data?.detail || 'Erreur lors de l\'accès au TP');
    } finally {
      setLoading(false);
    }
  };

  const stopVM = async () => {
    try {
      await API.post(`/vm/stop/${tpId}`);
      navigate('/dashboard');
    } catch (error) {
      console.error('Erreur lors de l\'arrêt de la VM:', error);
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  // Use the full `guacamole_url` returned by the backend when available.
  const iframeSrc = guacamoleUrl || `${GUAC_BASE}/`;

  if (loading) {
    return (
      <div className="lab-page">
        <div style={{ textAlign: 'center', padding: '50px' }}>
          <h2>⏳ Initialisation de la machine virtuelle...</h2>
          <p>Authentification CAS et connexion à Kali (machine 100)...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="lab-page">
        <div style={{ textAlign: 'center', padding: '50px', color: 'red' }}>
          <h2>❌ Erreur d'accès</h2>
          <p>{error}</p>
          <button onClick={() => navigate('/dashboard')}>Retour au tableau de bord</button>
        </div>
      </div>
    );
  }

  return (
    <div className="lab-page">
      <header className="lab-header">
        <h1>{tp?.title || 'TP en cours'}</h1>

        <div className="header-controls">
          <span>Chronomètre: {formatTime(timer)}</span>
          <button onClick={() => setShowInstructions(!showInstructions)}>
            Instructions
          </button>
          <button onClick={stopVM}>Arrêter la VM</button>
        </div>
      </header>

      <div className="lab-content">
        {showInstructions && (
          <div className="instructions-modal">
            <h2>Instructions</h2>
            <ReactMarkdown>{tp?.instructions || 'Instructions non disponibles.'}</ReactMarkdown>
            <button onClick={() => setShowInstructions(false)}>Fermer</button>
          </div>
        )}

        <div className="guacamole-container">
          {guacamoleUrl ? (
            <>
              <div style={{ 
                background: '#f0f0f0', 
                padding: '10px',
                marginBottom: '10px',
                borderRadius: '4px',
                fontSize: '12px'
              }}>
                ✅ Connecté en tant que: <strong>{guacamoleUrl.includes('username=') ? 
                  guacamoleUrl.split('username=')[1] : 'Utilisateur CAS'}</strong>
              </div>
              <iframe
                title="Guacamole"
                src={iframeSrc}
                style={{ width: '100%', height: '80vh', border: 0 }}
                allow="clipboard-read; clipboard-write"
              />
            </>
          ) : (
            <p>⏳ Démarrage de la VM...</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default LabPage;
