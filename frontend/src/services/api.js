import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:8000/api',
});

// Intercepteur pour ajouter le token JWT
API.interceptors.request.use(
  (config) => {
    let token = localStorage.getItem('token');

    // Ne pas utiliser les valeurs littérales 'undefined' ou 'null' (stockées par erreur)
    if (token === 'undefined' || token === 'null') {
      console.warn('⚠️ Token invalide dans localStorage, nettoyage...');
      localStorage.removeItem('token');
      token = null;
    }

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
      console.log('🔐 Token ajouté au header Authorization');
    } else {
      console.warn('⚠️ Pas de token correct dans localStorage!');
    }

    return config;
  },

  (error) => {
    return Promise.reject(error);
  }
);

// Intercepteur pour gérer 401 Unauthorized (token invalide)
API.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      console.warn('🔒 401 Unauthorized reçu - nettoyage du token et redirection vers login');
      localStorage.removeItem('token');
      localStorage.removeItem('user_id');
      localStorage.removeItem('username');
      localStorage.removeItem('role');
      window.location.href = '/';
    }
    return Promise.reject(error);
  }
);

export default API; 
