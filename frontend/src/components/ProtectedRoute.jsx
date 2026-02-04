import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

// allowedRoles can be a string or array of strings
const ProtectedRoute = ({ children, allowedRoles }) => {
  const { user } = useAuth();
  const location = useLocation();

  // If user is not authenticated, redirect to login preserving the attempted path
  if (!user) {
    const redirect = encodeURIComponent(location.pathname + location.search);
    return <Navigate to={`/?redirect=${redirect}`} replace />;
  }

  // If allowedRoles defined, enforce role-based access
  if (allowedRoles) {
    const roles = Array.isArray(allowedRoles) ? allowedRoles : [allowedRoles];
    const userRole = (user.role || '').toString().toLowerCase();
    const allowed = roles.map(r => r.toString().toLowerCase()).includes(userRole);
    if (!allowed) {
      // Redirect to a forbidden page
      return <Navigate to="/forbidden" replace />;
    }
  }

  return children;
};

export default ProtectedRoute;
 