import React, { useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';

const CallbackPage = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  useEffect(() => {
    const ticket = searchParams.get('ticket');
    
    if (ticket) {
      // Rediriger vers le backend pour traitement
      window.location.href = `http://localhost:8000/api/auth/callback?ticket=${ticket}`;
    } else {
      // Pas de ticket, retourner à la page de login
      navigate('/', { replace: true });
    }
  }, [searchParams, navigate]);

  return (
    <div style={{ 
      display: 'flex', 
      justifyContent: 'center', 
      alignItems: 'center', 
      height: '100vh',
      flexDirection: 'column'
    }}>
      <div style={{ fontSize: '24px', marginBottom: '20px' }}>⏳</div>
      <p>Authentification en cours...</p>
    </div>
  );
};

export default CallbackPage;