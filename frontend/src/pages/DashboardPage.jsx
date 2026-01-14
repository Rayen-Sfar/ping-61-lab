import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import API from '../services/api';
import TPList from '../components/TPList';

const DashboardPage = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [tps, setTps] = useState([]);

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
    }
  };

  const handleStartTP = (tpId) => {
    navigate(`/lab/${tpId}`);
  };

  return (
    <div className="dashboard">
      <header>
        <div className="header-content">
          <img src="image1.jpg" alt="Logo" className="logo" />
          <h1>Dashboard Étudiant</h1>
        </div>
        <button onClick={logout}>Déconnexion</button>
      </header>
      <TPList tps={tps} onStartTP={handleStartTP} />
    </div>
  );
};

export default DashboardPage; 
