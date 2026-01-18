import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import API from '../services/api';
import '../styles/AdminPage.css';

const AdminPage = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [tps, setTps] = useState([]);
  const [loading, setLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    instructions: '',
    difficulty: 'Moyen',
    duration: '2h',
    vm_type: 'Linux',
    status: 'Published'
  });

  useEffect(() => {
    if (!user) {
      navigate('/');
      return;
    }
    fetchTPs();
  }, [user, navigate]);

  const fetchTPs = async () => {
    try {
      const response = await API.get('/tp');
      setTps(response.data);
    } catch (error) {
      console.error('Error fetching TPs:', error);
      setErrorMessage('Erreur lors du chargement des TPs');
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrorMessage('');
    setSuccessMessage('');

    try {
      const tpData = {
        ...formData,
        created_by: user.username || 'Enseignant'
      };
      await API.post('/tp', tpData);
      setSuccessMessage('TP créé avec succès !');
      setFormData({
        title: '',
        description: '',
        instructions: '',
        difficulty: 'Moyen',
        duration: '2h',
        vm_type: 'Linux',
        status: 'Published'
      });
      setShowForm(false);
      fetchTPs();
    } catch (error) {
      console.error('Error creating TP:', error);
      setErrorMessage('Erreur lors de la création du TP');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteTP = async (tpId) => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer ce TP ?')) {
      try {
        await API.delete(`/tp/${tpId}`);
        setSuccessMessage('TP supprimé avec succès !');
        fetchTPs();
      } catch (error) {
        console.error('Error deleting TP:', error);
        setErrorMessage('Erreur lors de la suppression du TP');
      }
    }
  };

  return (
    <div className="admin-page">
      <header className="admin-header">
        <div className="header-content">
          <h1>🏫 Espace Enseignant - Gestion des TPs</h1>
          <div className="header-actions">
            <span className="welcome-text">Bienvenue, {user?.username}</span>
            <button onClick={logout} className="btn-logout">Déconnexion</button>
          </div>
        </div>
      </header>

      <div className="admin-container">
        {/* Messages */}
        {successMessage && <div className="alert alert-success">{successMessage}</div>}
        {errorMessage && <div className="alert alert-error">{errorMessage}</div>}

        {/* Bouton pour afficher/masquer le formulaire */}
        <div className="form-toggle">
          <button 
            className="btn-primary"
            onClick={() => setShowForm(!showForm)}
          >
            {showForm ? '❌ Fermer le formulaire' : '➕ Ajouter un nouveau TP'}
          </button>
        </div>

        {/* Formulaire d'ajout de TP */}
        {showForm && (
          <div className="add-tp-form-section">
            <h2>Créer un nouveau TP</h2>
            <form onSubmit={handleSubmit} className="add-tp-form">
              <div className="form-group">
                <label htmlFor="title">Titre du TP *</label>
                <input
                  type="text"
                  id="title"
                  name="title"
                  value={formData.title}
                  onChange={handleInputChange}
                  placeholder="Ex: TP 1 - Introduction à Linux"
                  required
                  className="form-input"
                />
              </div>

              <div className="form-group">
                <label htmlFor="description">Description *</label>
                <textarea
                  id="description"
                  name="description"
                  value={formData.description}
                  onChange={handleInputChange}
                  placeholder="Décrivez l'objectif du TP"
                  required
                  rows="4"
                  className="form-textarea"
                />
              </div>

              <div className="form-group">
                <label htmlFor="instructions">Instructions *</label>
                <textarea
                  id="instructions"
                  name="instructions"
                  value={formData.instructions}
                  onChange={handleInputChange}
                  placeholder="Détaillez les étapes du TP (vous pouvez utiliser Markdown)"
                  required
                  rows="6"
                  className="form-textarea"
                />
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="difficulty">Difficulté</label>
                  <select
                    id="difficulty"
                    name="difficulty"
                    value={formData.difficulty}
                    onChange={handleInputChange}
                    className="form-select"
                  >
                    <option>Facile</option>
                    <option>Moyen</option>
                    <option>Difficile</option>
                  </select>
                </div>

                <div className="form-group">
                  <label htmlFor="duration">Durée estimée</label>
                  <select
                    id="duration"
                    name="duration"
                    value={formData.duration}
                    onChange={handleInputChange}
                    className="form-select"
                  >
                    <option>1h</option>
                    <option>2h</option>
                    <option>3h</option>
                    <option>4h</option>
                  </select>
                </div>

                <div className="form-group">
                  <label htmlFor="vm_type">Type de VM</label>
                  <select
                    id="vm_type"
                    name="vm_type"
                    value={formData.vm_type}
                    onChange={handleInputChange}
                    className="form-select"
                  >
                    <option>Linux</option>
                    <option>Windows</option>
                    <option>Docker</option>
                    <option>Kubernetes</option>
                  </select>
                </div>
              </div>

              <div className="form-group">
                <label htmlFor="status">Statut</label>
                <select
                  id="status"
                  name="status"
                  value={formData.status}
                  onChange={handleInputChange}
                  className="form-select"
                >
                  <option>Published</option>
                  <option>Draft</option>
                  <option>Archived</option>
                </select>
              </div>

              <button type="submit" disabled={loading} className="btn-submit">
                {loading ? '⏳ Création en cours...' : '✅ Créer le TP'}
              </button>
            </form>
          </div>
        )}

        {/* Liste des TPs */}
        <div className="tps-list-section">
          <h2>📚 Liste des TPs ({tps.length})</h2>
          {tps.length === 0 ? (
            <p className="empty-message">Aucun TP créé pour le moment. Commencez par en ajouter un !</p>
          ) : (
            <div className="tps-grid">
              {tps.map(tp => (
                <div key={tp.id} className="tp-card">
                  <div className="tp-header">
                    <h3>{tp.title}</h3>
                    <span className={`status-badge ${tp.status.toLowerCase()}`}>
                      {tp.status}
                    </span>
                  </div>
                  
                  <p className="tp-description">{tp.description}</p>
                  
                  <div className="tp-meta">
                    <span className="meta-item">
                      <strong>Difficulté:</strong> {tp.difficulty}
                    </span>
                    <span className="meta-item">
                      <strong>Durée:</strong> {tp.duration}
                    </span>
                    <span className="meta-item">
                      <strong>VM:</strong> {tp.vm_type}
                    </span>
                  </div>

                  <div className="tp-footer">
                    <small>Par {tp.created_by}</small>
                    <button
                      onClick={() => handleDeleteTP(tp.id)}
                      className="btn-delete"
                    >
                      🗑️ Supprimer
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AdminPage;
