import React, { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import API from '../services/api';
import '../styles/DashboardPage.css';

const DashboardPage = () => {
  const { user, logout, setUser, setToken } = useAuth();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [tps, setTps] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    // Vérifier si on arrive avec des paramètres d'authentification CAS
    const token = searchParams.get('token');
    const userId = searchParams.get('user_id');
    const username = searchParams.get('username');
    const role = searchParams.get('role');
    const authError = searchParams.get('error');

    // Si erreur d'authentification, rediriger vers login
    if (authError === 'auth_failed') {
      navigate('/?error=Authentification échouée', { replace: true });
      return;
    }

    if (token && userId && username && role) {
      // Stocker les informations d'authentification
      localStorage.setItem('token', token);
      localStorage.setItem('user_id', userId);
      localStorage.setItem('username', username);
      localStorage.setItem('role', role);

      // Mettre à jour le contexte
      setToken(token);
      setUser({ id: userId, username, role });

      // Nettoyer l'URL
      navigate('/dashboard', { replace: true });
      return;
    }

    if (!user) {
      navigate('/');
      return;
    }
    fetchTPs();
  }, [user, navigate, searchParams, setUser, setToken]);

  const fetchTPs = async () => {
    try {
      setLoading(true);
      const response = await API.get('/tp');
      setTps(response.data || []);
      setError('');
    } catch (error) {
      console.error('Error fetching TPs:', error);
      setError('Erreur lors du chargement des TPs');
      setTps([]);
    } finally {
      setLoading(false);
    }
  };

  const handleStartTP = (tpId) => {
    navigate(`/lab/${tpId}`);
  };

  const goToAdminPage = () => {
    navigate('/admin');
  };

  return (
    <div className="dashboard-page">
      <header className="dashboard-header">
        <div className="header-content">
          <div className="header-left">
            <h1>📚 Lab on Demand - Dashboard</h1>
            <p className="subtitle">Bienvenue {user?.username}</p>
          </div>
          <div className="header-actions">
            <button onClick={goToAdminPage} className="btn-admin">
              🏫 Espace Enseignant
            </button>
            <button onClick={logout} className="btn-logout">
              Déconnexion
            </button>
          </div>
        </div>
      </header>

      <div className="dashboard-container">
        {error && <div className="alert alert-error">{error}</div>}

        {loading ? (
          <div className="loading-container">
            <div className="spinner"></div>
            <p>Chargement des TPs...</p>
          </div>
        ) : tps.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">📭</div>
            <h2>Aucun TP disponible</h2>
            <p>Les TPs seront bientôt disponibles. Veuillez vérifier plus tard.</p>
            <button onClick={goToAdminPage} className="btn-admin">
              🏫 Créer un TP
            </button>
          </div>
        ) : (
          <div className="tps-container">
            <h2>Travaux Pratiques Disponibles ({tps.length})</h2>
            <div className="tps-grid">
              {tps.map(tp => (
                <div key={tp.id} className="tp-card-dashboard">
                  <div className="tp-card-header">
                    <h3>{tp.title}</h3>
                    <span className={`difficulty-badge ${tp.difficulty.toLowerCase()}`}>
                      {tp.difficulty}
                    </span>
                  </div>
                  <p className="tp-description">{tp.description}</p>
                  <div className="tp-info">
                    <div className="info-item">
                      <span className="info-label">⏱️ Durée:</span>
                      <span className="info-value">{tp.duration}</span>
                    </div>
                    <div className="info-item">
                      <span className="info-label">💻 Type VM:</span>
                      <span className="info-value">{tp.vm_type}</span>
                    </div>
                    <div className="info-item">
                      <span className="info-label">👨🏫 Créé par:</span>
                      <span className="info-value">{tp.created_by}</span>
                    </div>
                  </div>
                  <button
                    onClick={() => handleStartTP(tp.id)}
                    className="btn-start-tp"
                  >
                    ▶️ Commencer le TP
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default DashboardPage;