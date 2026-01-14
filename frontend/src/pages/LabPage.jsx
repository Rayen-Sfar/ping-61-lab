import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import API from '../services/api';
import GuacamoleDisplay from '../components/GuacamoleDisplay';

const LabPage = () => {
  const { tpId } = useParams();
  const navigate = useNavigate();
  const [tp, setTp] = useState(null);
  const [guacamoleUrl, setGuacamoleUrl] = useState('');
  const [timer, setTimer] = useState(0);
  const [showInstructions, setShowInstructions] = useState(false);

  useEffect(() => {
    fetchTP();
    startVM();
    const interval = setInterval(() => setTimer(t => t + 1), 1000);
    return () => clearInterval(interval);
  }, [tpId]);

  const fetchTP = async () => {
    try {
      const response = await API.get(`/tp/${tpId}`);
      setTp(response.data);
    } catch (error) {
      console.error('Error fetching TP:', error);
    }
  };

  const startVM = async () => {
    try {
      const response = await API.post(`/vm/start/${tpId}`);
      setGuacamoleUrl(response.data.guacamole_url);
    } catch (error) {
      console.error('Error starting VM:', error);
    }
  };

  const stopVM = async () => {
    try {
      await API.post(`/vm/stop/${tpId}`);
      navigate('/dashboard');
    } catch (error) {
      console.error('Error stopping VM:', error);
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  // Extraire le token de connexion depuis l'URL Guacamole
  const getConnectionToken = () => {
    if (!guacamoleUrl) return '';
    const urlParts = guacamoleUrl.split('/#/client/');
    return urlParts[1] || '';
  };

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
            <GuacamoleDisplay connectionToken={getConnectionToken()} />
          ) : (
            <p>Démarrage de la VM...</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default LabPage; 
