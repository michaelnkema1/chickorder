import { Navigate } from 'react-router-dom';

const ProtectedRoute = ({ children, user, adminOnly = false }) => {
  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (adminOnly && !user.is_admin) {
    return <Navigate to="/" replace />;
  }

  return children;
};

export default ProtectedRoute;

