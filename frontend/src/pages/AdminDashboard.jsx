import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { adminAPI } from '../services/api';
import toast from 'react-hot-toast';

const AdminDashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const response = await adminAPI.getDashboard();
      setStats(response.data);
    } catch (error) {
      toast.error('Failed to load dashboard stats');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center">Loading dashboard...</div>
      </div>
    );
  }

  if (!stats) {
    return null;
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-4xl font-bold">Admin Dashboard</h1>
        <Link to="/admin/orders" className="btn btn-primary">
          Manage Orders
        </Link>
      </div>

      {/* Stats Grid */}
      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="card">
          <div className="text-sm text-gray-600 mb-1">Total Orders</div>
          <div className="text-3xl font-bold text-primary-600">{stats.total_orders}</div>
        </div>
        <div className="card">
          <div className="text-sm text-gray-600 mb-1">Pending Orders</div>
          <div className="text-3xl font-bold text-yellow-600">{stats.pending_orders}</div>
        </div>
        <div className="card">
          <div className="text-sm text-gray-600 mb-1">Completed Orders</div>
          <div className="text-3xl font-bold text-green-600">{stats.completed_orders}</div>
        </div>
        <div className="card">
          <div className="text-sm text-gray-600 mb-1">Total Revenue</div>
          <div className="text-3xl font-bold text-primary-600">
            GHS {stats.total_revenue.toFixed(2)}
          </div>
        </div>
      </div>

      {/* Additional Stats */}
      <div className="grid md:grid-cols-3 gap-6">
        <div className="card">
          <div className="text-sm text-gray-600 mb-1">Today's Revenue</div>
          <div className="text-2xl font-bold text-primary-600">
            GHS {stats.today_revenue.toFixed(2)}
          </div>
        </div>
        <div className="card">
          <div className="text-sm text-gray-600 mb-1">Average Wait Time</div>
          <div className="text-2xl font-bold text-primary-600">
            {stats.average_wait_time
              ? `${stats.average_wait_time.toFixed(1)} min`
              : 'N/A'}
          </div>
        </div>
        <div className="card">
          <div className="text-sm text-gray-600 mb-1">Digital Payments</div>
          <div className="text-2xl font-bold text-primary-600">
            {stats.digital_payment_percentage.toFixed(1)}%
          </div>
        </div>
      </div>

      {/* Success Metrics */}
      <div className="card mt-8">
        <h2 className="text-2xl font-semibold mb-4">MVP Success Metrics</h2>
        <div className="grid md:grid-cols-2 gap-4">
          <div>
            <div className="flex justify-between items-center mb-2">
              <span>Wait Time Reduction (Target: 50%)</span>
              <span className="font-semibold">
                {stats.average_wait_time ? 'Calculating...' : 'N/A'}
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div className="bg-primary-600 h-2 rounded-full" style={{ width: '50%' }}></div>
            </div>
          </div>
          <div>
            <div className="flex justify-between items-center mb-2">
              <span>Digital Payments (Target: 60%)</span>
              <span className="font-semibold">
                {stats.digital_payment_percentage.toFixed(1)}%
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-primary-600 h-2 rounded-full"
                style={{ width: `${Math.min(stats.digital_payment_percentage, 100)}%` }}
              ></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;

