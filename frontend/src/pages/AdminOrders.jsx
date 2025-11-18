import { useState, useEffect } from 'react';
import { adminAPI, ordersAPI } from '../services/api';
import toast from 'react-hot-toast';

const AdminOrders = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadOrders();
  }, []);

  const loadOrders = async () => {
    try {
      const response = await adminAPI.getPendingOrders();
      setOrders(response.data);
    } catch (error) {
      toast.error('Failed to load orders');
    } finally {
      setLoading(false);
    }
  };

  const updateOrderStatus = async (orderId, newStatus) => {
    try {
      await ordersAPI.updateStatus(orderId, { status: newStatus });
      toast.success('Order status updated');
      loadOrders();
    } catch (error) {
      toast.error('Failed to update order status');
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      pending: 'bg-yellow-100 text-yellow-800',
      confirmed: 'bg-blue-100 text-blue-800',
      preparing: 'bg-purple-100 text-purple-800',
      ready: 'bg-green-100 text-green-800',
      completed: 'bg-gray-100 text-gray-800',
      cancelled: 'bg-red-100 text-red-800',
    };
    return colors[status] || colors.pending;
  };

  const getNextStatus = (currentStatus) => {
    const statusFlow = {
      pending: 'confirmed',
      confirmed: 'preparing',
      preparing: 'ready',
      ready: 'completed',
    };
    return statusFlow[currentStatus];
  };

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center">Loading orders...</div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <h1 className="text-4xl font-bold mb-8">Manage Orders</h1>

      {orders.length === 0 ? (
        <div className="card text-center py-12">
          <p className="text-gray-500 text-lg">No pending orders</p>
        </div>
      ) : (
        <div className="space-y-4">
          {orders.map((order) => {
            const nextStatus = getNextStatus(order.status);
            return (
              <div key={order.id} className="card">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-xl font-semibold">Order #{order.order_number}</h3>
                    <p className="text-gray-600">
                      {order.customer_name} • {order.customer_phone}
                    </p>
                    <p className="text-sm text-gray-500">
                      {new Date(order.created_at).toLocaleString()}
                    </p>
                  </div>
                  <span className={`px-4 py-2 rounded-full font-semibold ${getStatusColor(order.status)}`}>
                    {order.status.charAt(0).toUpperCase() + order.status.slice(1)}
                  </span>
                </div>

                <div className="mb-4">
                  <h4 className="font-semibold mb-2">Items:</h4>
                  <div className="space-y-1">
                    {order.items.map((item) => (
                      <div key={item.id} className="flex justify-between text-sm">
                        <span>
                          {item.product_name} × {item.quantity}
                          {item.customization && ` (${item.customization})`}
                        </span>
                        <span className="font-semibold">GHS {item.subtotal.toFixed(2)}</span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="flex justify-between items-center border-t pt-4">
                  <div>
                    <span className="text-gray-600">Total: </span>
                    <span className="text-xl font-bold text-primary-600">
                      GHS {order.total_amount.toFixed(2)}
                    </span>
                  </div>
                  {nextStatus && (
                    <button
                      onClick={() => updateOrderStatus(order.id, nextStatus)}
                      className="btn btn-primary"
                    >
                      Mark as {nextStatus.charAt(0).toUpperCase() + nextStatus.slice(1)}
                    </button>
                  )}
                  {order.status === 'ready' && (
                    <button
                      onClick={() => updateOrderStatus(order.id, 'completed')}
                      className="btn btn-primary"
                    >
                      Mark as Completed
                    </button>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default AdminOrders;

