import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import { AuthProvider } from './context/AuthContext';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import LabPage from './pages/LabPage';
import AdminPage from './pages/AdminPage';
import CallbackPage from './pages/CallbackPage';
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <Routes>
            <Route path="/" element={<LoginPage />} />

            {/* Protected Routes - require authentication */}
            <Route
              path="/dashboard"
              element={<ProtectedRoute><DashboardPage /></ProtectedRoute>}
            />
            <Route
              path="/lab/:tpId"
              element={<ProtectedRoute><LabPage /></ProtectedRoute>}
            />
            <Route
              path="/admin"
              element={<ProtectedRoute allowedRoles={["teacher","admin"]}><AdminPage /></ProtectedRoute>}
            />
            <Route path="/forbidden" element={<ProtectedRoute><div style={{padding: '40px', textAlign: 'center'}}><h1>🔒 Accès refusé</h1><p>Vous n'êtes pas autorisé à accéder à cette page.</p></div></ProtectedRoute>} />

            {/* Callback must remain accessible for OAuth flow */}
            <Route path="/api/auth/callback" element={<CallbackPage />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App; 
