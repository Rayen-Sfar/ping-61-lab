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
    // Si pas d'utilisateur, rediriger vers login
    if (!user) {
      navigate('/');
      return;
    }
    
    console.log('👤 User authentifié:', user.username);
    fetchTPs();
  }, [user, navigate]);

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
            {/* Montrer le bouton admin seulement si rôle enseignant/admin */}
            {['teacher', 'admin'].includes((user?.role || '').toString().toLowerCase()) && (
              <button onClick={goToAdminPage} className="btn-admin">
                🏫 Espace Enseignant
              </button>
            )}
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