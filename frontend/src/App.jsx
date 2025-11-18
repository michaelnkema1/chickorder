import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { useState, useEffect } from 'react';
import { authAPI } from './services/api';

// Pages
import Home from './pages/Home';
import Products from './pages/Products';
import Order from './pages/Order';
import OrderTracking from './pages/OrderTracking';
import Login from './pages/Login';
import Register from './pages/Register';
import AdminDashboard from './pages/AdminDashboard';
import AdminOrders from './pages/AdminOrders';

// Components
import Navbar from './components/Navbar';
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      authAPI.getMe()
        .then((response) => {
          setUser(response.data);
        })
        .catch(() => {
          localStorage.removeItem('token');
          localStorage.removeItem('user');
        })
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const handleLogin = (userData, token) => {
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(userData));
    setUser(userData);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Loading...</div>
      </div>
    );
  }

  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navbar user={user} onLogout={handleLogout} />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/products" element={<Products />} />
          <Route path="/order" element={<Order user={user} />} />
          <Route path="/order/:orderId" element={<OrderTracking />} />
          <Route
            path="/login"
            element={user ? <Navigate to="/" /> : <Login onLogin={handleLogin} />}
          />
          <Route
            path="/register"
            element={user ? <Navigate to="/" /> : <Register onLogin={handleLogin} />}
          />
          <Route
            path="/admin"
            element={
              <ProtectedRoute user={user} adminOnly>
                <AdminDashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin/orders"
            element={
              <ProtectedRoute user={user} adminOnly>
                <AdminOrders />
              </ProtectedRoute>
            }
          />
        </Routes>
        <Toaster position="top-right" />
      </div>
    </Router>
  );
}

export default App;

