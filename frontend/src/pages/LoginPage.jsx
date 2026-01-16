 
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import '../styles/LoginPage.css';

export default function LoginPage() {
  const navigate = useNavigate();
  const { setUser, setToken } = useAuth();
  const [formData, setFormData] = useState({
    identifiant: '',
    motDePasse: '',
    sesouvenir: false
  });
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!formData.identifiant || !formData.motDePasse) {
      alert('Veuillez remplir tous les champs');
      return;
    }

    setLoading(true);
    
    // Simuler un utilisateur connecté
    setTimeout(() => {
      const mockToken = "mock-jwt-token";
      const mockUser = { id: "1", role: "student", username: formData.identifiant };
      
      // Stocker dans localStorage
      localStorage.setItem('token', mockToken);
      localStorage.setItem('user_id', mockUser.id);
      localStorage.setItem('role', mockUser.role);
      localStorage.setItem('username', mockUser.username);
      
      // Mettre à jour contexte
      setToken(mockToken);
      setUser(mockUser);
      
      // Rediriger vers dashboard
      navigate('/dashboard');
    }, 500);
  };

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
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
            <h1 className="login-title">Esigelec</h1>
          </div>

          {/* Formulaire */}
          <form onSubmit={handleSubmit} className="login-form">
            <div className="form-section">
              <p className="form-subtitle">
                <strong>🔐</strong> Entrez votre identifiant et votre mot de passe.
              </p>

              {/* Champ Identifiant */}
              <div className="form-group">
                <label htmlFor="identifiant">Identifiant <span className="required">*</span></label>
                <input
                  type="text"
                  id="identifiant"
                  name="identifiant"
                  value={formData.identifiant}
                  onChange={handleInputChange}
                  placeholder="Vous devez entrer votre identifiant."
                  className="form-input"
                  disabled={loading}
                />
              </div>

              {/* Champ Mot de passe */}
              <div className="form-group">
                <label htmlFor="motDePasse">Mot de passe <span className="required">*</span></label>
                <div className="password-input-wrapper">
                  <input
                    type={showPassword ? "text" : "password"}
                    id="motDePasse"
                    name="motDePasse"
                    value={formData.motDePasse}
                    onChange={handleInputChange}
                    placeholder="Vous devez entrer votre mot de passe."
                    className="form-input"
                    disabled={loading}
                  />
                  <button
                    type="button"
                    className="password-toggle"
                    onClick={togglePasswordVisibility}
                    disabled={loading}
                  >
                    {showPassword ? '🙈' : '👁️'}
                  </button>
                </div>
              </div>

              {/* Checkbox Se souvenir */}
              <div className="checkbox-group">
                <input
                  type="checkbox"
                  id="sesouvenir"
                  name="sesouvenir"
                  checked={formData.sesouvenir}
                  onChange={handleInputChange}
                  disabled={loading}
                />
                <label htmlFor="sesouvenir">Se souvenir de moi</label>
              </div>

              {/* Bouton Connexion */}
              <button
                type="submit"
                className="btn-connect"
                disabled={loading}
              >
                {loading ? 'Connexion en cours...' : 'SE CONNECTER'}
              </button>
            </div>

            {/* Liens supplémentaires */}
            <div className="login-links">
              <div className="link-group">
                <span>👤 Vous êtes déjà élève ?</span>
                <a href="#forgot">Mot de passe oublié / expiré ?</a> | 
                <a href="#change"> Changer votre mot de passe</a>
              </div>
              <div className="link-group">
                <span>Futur élève en phase d'admission ou référent ?</span>
                <a href="#future"> Se connecter ici</a>
              </div>
            </div>
          </form>
        </div>
      </div>

      {/* Background image */}
      <div className="login-background"></div>
    </div>
  );
}