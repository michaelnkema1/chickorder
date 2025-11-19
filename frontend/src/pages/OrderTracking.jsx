import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ordersAPI } from '../services/api';
import MobileMoneyPrompt from '../components/MobileMoneyPrompt';
import toast from 'react-hot-toast';

const OrderTracking = () => {
  const { orderId } = useParams();
  const navigate = useNavigate();
  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showMobileMoneyPrompt, setShowMobileMoneyPrompt] = useState(false);
  const [processingPayment, setProcessingPayment] = useState(false);

  useEffect(() => {
    loadOrder();
  }, [orderId]);

  const loadOrder = async () => {
    try {
      const response = await ordersAPI.getById(orderId);
      setOrder(response.data);
    } catch (error) {
      toast.error('Failed to load order');
    } finally {
      setLoading(false);
    }
  };

  const handlePayment = async (paymentMethod) => {
    if (!order) {
      toast.error('Order not loaded');
      return;
    }

    // Check if payment is already processing or completed
    if (order.payment_status === 'processing' || order.payment_status === 'completed') {
      toast('Payment has already been initiated for this order', { icon: 'ℹ️' });
      return;
    }

    try {
      setProcessingPayment(true);
      console.log('Initiating payment:', { orderId: order.id, paymentMethod });
      
      const response = await ordersAPI.initiatePayment(order.id, paymentMethod);
      console.log('Payment response:', response.data);
      
      // If payment URL is provided, redirect to it
      if (response.data.payment_url) {
        window.location.href = response.data.payment_url;
      } else if (paymentMethod === 'mobile_money') {
        // Show mobile money verification prompt
        if (response.data.message) {
          toast.success(response.data.message, { duration: 5000 });
        }
        setShowMobileMoneyPrompt(true);
        loadOrder(); // Reload order to get updated payment status
      } else if (paymentMethod === 'cash') {
        // For cash, just update the order
        toast.success('Payment will be collected when you pickup your order!');
        loadOrder(); // Reload order to get updated payment status
      }
    } catch (error) {
      console.error('Payment error:', error);
      console.error('Error response:', error.response);
      const errorMessage = error.response?.data?.detail || error.message || 'Failed to initiate payment';
      console.error('Full error details:', {
        message: error.message,
        response: error.response?.data,
        status: error.response?.status
      });
      toast.error(errorMessage);
    } finally {
      setProcessingPayment(false);
    }
  };

  const handleMobileMoneyComplete = async () => {
    setShowMobileMoneyPrompt(false);
    
    // In production, this would be handled by the payment gateway callback
    // For now, we'll simulate payment completion
    // You can manually mark as completed via admin panel or API
    
    toast.success('Mobile money payment verification completed!');
    loadOrder(); // Reload order to get updated payment status
  };

  const getStatusColor = (status) => {
    const colors = {
      pending: 'bg-yellow-100 text-yellow-800',
      confirmed: 'bg-blue-100 text-blue-800',
      ready: 'bg-green-100 text-green-800',
      completed: 'bg-gray-100 text-gray-800',
      cancelled: 'bg-red-100 text-red-800',
    };
    return colors[status] || colors.pending;
  };

  const getStatusSteps = () => {
    if (!order) return [];
    const steps = [
      { key: 'pending', label: 'Order Placed' },
      { key: 'confirmed', label: 'Confirmed' },
      { key: 'ready', label: 'Ready for Pickup' },
      { key: 'completed', label: 'Completed' },
    ];
    return steps;
  };

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center">Loading order...</div>
      </div>
    );
  }

  if (!order) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center">Order not found</div>
      </div>
    );
  }

  const statusSteps = getStatusSteps();
  const currentStatusIndex = statusSteps.findIndex((s) => s.key === order.status);

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <h1 className="text-4xl font-bold mb-8">Order Tracking</h1>
        <p className="text-lg text-gray-600 mb-6">
          Track your live chicken order. We'll notify you via SMS when your chickens are killed, dressed, and ready for pickup.
        </p>

      <div className="card mb-6">
        <div className="flex justify-between items-start mb-4">
          <div>
            <h2 className="text-2xl font-semibold">Order #{order.order_number}</h2>
            <p className="text-gray-600">
              Placed on {new Date(order.created_at).toLocaleString()}
            </p>
          </div>
          <span className={`px-4 py-2 rounded-full font-semibold ${getStatusColor(order.status)}`}>
            {order.status.charAt(0).toUpperCase() + order.status.slice(1)}
          </span>
        </div>

        {/* Status Progress */}
        <div className="mb-6">
          <div className="flex items-center justify-between mb-4">
            {statusSteps.map((step, index) => (
              <div key={step.key} className="flex-1 flex items-center">
                <div className="flex flex-col items-center flex-1">
                  <div
                    className={`w-12 h-12 rounded-full flex items-center justify-center font-bold ${
                      index <= currentStatusIndex
                        ? 'bg-primary-600 text-white'
                        : 'bg-gray-200 text-gray-500'
                    }`}
                  >
                    {index + 1}
                  </div>
                  <span className="mt-2 text-sm text-center">{step.label}</span>
                </div>
                {index < statusSteps.length - 1 && (
                  <div
                    className={`flex-1 h-1 mx-2 ${
                      index < currentStatusIndex ? 'bg-primary-600' : 'bg-gray-200'
                    }`}
                  />
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Order Items */}
        <div className="mb-6">
          <h3 className="text-lg font-semibold mb-4">Order Items</h3>
          <div className="space-y-3">
            {order.items.map((item) => (
              <div key={item.id} className="flex justify-between items-center border-b pb-3">
                <div>
                  <p className="font-semibold">{item.product_name}</p>
                  <p className="text-sm text-gray-600">
                    Quantity: {item.quantity}
                    {item.customization && ` • ${item.customization}`}
                  </p>
                </div>
                <span className="font-semibold">GHS {item.subtotal.toFixed(2)}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Order Summary */}
        <div className="border-t pt-4">
          <div className="flex justify-between items-center mb-2">
            <span className="text-gray-600">Subtotal</span>
            <span className="font-semibold">GHS {order.total_amount.toFixed(2)}</span>
          </div>
          <div className="flex justify-between items-center text-xl font-bold">
            <span>Total</span>
            <span className="text-primary-600">GHS {order.total_amount.toFixed(2)}</span>
          </div>
        </div>

        {/* Customer Info */}
        <div className="mt-6 pt-6 border-t">
          <h3 className="text-lg font-semibold mb-4">Customer Information</h3>
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <p className="text-sm text-gray-600">Name</p>
              <p className="font-semibold">{order.customer_name}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Phone</p>
              <p className="font-semibold">{order.customer_phone}</p>
            </div>
            {order.customer_email && (
              <div>
                <p className="text-sm text-gray-600">Email</p>
                <p className="font-semibold">{order.customer_email}</p>
              </div>
            )}
            <div>
              <p className="text-sm text-gray-600">Payment Status</p>
              <p className="font-semibold capitalize">{order.payment_status}</p>
            </div>
            {order.payment_method && (
              <div>
                <p className="text-sm text-gray-600">Payment Method</p>
                <p className="font-semibold capitalize">{order.payment_method.replace('_', ' ')}</p>
              </div>
            )}
          </div>
        </div>

        {/* Payment Section */}
        {(order.payment_status === 'pending' || !order.payment_status) && (
          <div className="card mt-6">
            <h3 className="text-xl font-semibold mb-4">Complete Payment</h3>
            <p className="text-gray-600 mb-4">
              Choose a payment method to complete your order:
            </p>
            <div className="grid md:grid-cols-2 gap-4">
              <button
                onClick={() => handlePayment('cash')}
                disabled={processingPayment}
                className="btn btn-outline p-4 text-left"
              >
                <div className="font-semibold mb-1">💵 Cash on Arrival</div>
                <div className="text-sm text-gray-600">Pay when you pickup your order</div>
              </button>
              <button
                onClick={() => handlePayment('mobile_money')}
                disabled={processingPayment}
                className="btn btn-outline p-4 text-left"
              >
                <div className="font-semibold mb-1">📱 Mobile Money</div>
                <div className="text-sm text-gray-600">Pay via mobile money (MTN/Vodafone/AirtelTigo)</div>
              </button>
            </div>
            {processingPayment && (
              <div className="mt-4 text-center text-gray-600">
                Processing payment...
              </div>
            )}
          </div>
        )}

        {order.payment_status === 'processing' && (
          <div className="card mt-6 bg-yellow-50 border-yellow-200">
            <h3 className="text-xl font-semibold mb-2 text-yellow-800">Payment Processing</h3>
            <p className="text-yellow-700">
              Your payment is being processed. You'll be notified once it's confirmed.
            </p>
            {order.payment_reference && (
              <p className="text-sm text-yellow-600 mt-2">
                Reference: {order.payment_reference}
              </p>
            )}
          </div>
        )}

        {order.payment_status === 'completed' && (
          <div className="card mt-6 bg-green-50 border-green-200">
            <h3 className="text-xl font-semibold mb-2 text-green-800">✅ Payment Completed</h3>
            <p className="text-green-700">
              Your payment has been confirmed. Your order is being prepared.
            </p>
          </div>
        )}

        {order.notes && (
          <div className="mt-6 pt-6 border-t">
            <p className="text-sm text-gray-600 mb-2">Notes</p>
            <p className="font-semibold">{order.notes}</p>
          </div>
        )}
      </div>

      {/* Mobile Money Verification Prompt */}
      {showMobileMoneyPrompt && order && (
        <MobileMoneyPrompt
          order={order}
          phone={order.customer_phone}
          amount={order.total_amount}
          onComplete={handleMobileMoneyComplete}
          onCancel={() => setShowMobileMoneyPrompt(false)}
        />
      )}
    </div>
  );
};

export default OrderTracking;

