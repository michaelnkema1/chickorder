import { useState } from 'react';
import { Link } from 'react-router-dom';
import { authAPI } from '../services/api';
import toast from 'react-hot-toast';

const Login = ({ onLogin }) => {
  const [formData, setFormData] = useState({
    email: '',
    phone: '',
    password: '',
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.password || (!formData.email && !formData.phone)) {
      toast.error('Please fill in all required fields');
      return;
    }

    try {
      setLoading(true);
      const response = await authAPI.login(formData);
      const { access_token } = response.data;
      
      // Store token first so getMe can use it
      localStorage.setItem('token', access_token);
      
      // Get user info
      const userResponse = await authAPI.getMe();
      onLogin(userResponse.data, access_token);
      toast.success('Login successful!');
    } catch (error) {
      console.error('Login error:', error);
      toast.error(error.response?.data?.detail || 'Login failed');
      // Clear token if login failed
      localStorage.removeItem('token');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="card">
        <h1 className="text-3xl font-bold mb-6 text-center">Login</h1>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="label">Email or Phone</label>
            <input
              type="text"
              className="input"
              placeholder="Enter email or phone"
              value={formData.email || formData.phone}
              onChange={(e) => {
                const value = e.target.value;
                if (value.includes('@')) {
                  setFormData({ ...formData, email: value, phone: '' });
                } else {
                  setFormData({ ...formData, phone: value, email: '' });
                }
              }}
              required
            />
          </div>
          
          <div>
            <label className="label">Password</label>
            <input
              type="password"
              className="input"
              placeholder="Enter password"
              value={formData.password}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              required
            />
          </div>

          <button
            type="submit"
            className="btn btn-primary w-full"
            disabled={loading}
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-gray-600">
            Don't have an account?{' '}
            <Link to="/register" className="text-primary-600 hover:underline">
              Register here
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;

