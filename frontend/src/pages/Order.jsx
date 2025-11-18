import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { productsAPI, ordersAPI } from '../services/api';
import toast from 'react-hot-toast';

const Order = ({ user }) => {
  const [products, setProducts] = useState([]);
  const [cart, setCart] = useState([]);
  const [customerInfo, setCustomerInfo] = useState({
    customer_name: user?.name || '',
    customer_phone: user?.phone || '',
    customer_email: user?.email || '',
  });
  const [paymentMethod, setPaymentMethod] = useState('cash');
  const [notes, setNotes] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    loadProducts();
  }, []);

  const loadProducts = async () => {
    try {
      const response = await productsAPI.getAll({ available_only: true });
      setProducts(response.data);
    } catch (error) {
      toast.error('Failed to load products');
    }
  };

  const addToCart = (product) => {
    const existingItem = cart.find((item) => item.product_id === product.id);
    if (existingItem) {
      setCart(
        cart.map((item) =>
          item.product_id === product.id
            ? { ...item, quantity: item.quantity + 1 }
            : item
        )
      );
    } else {
      setCart([
        ...cart,
        {
          product_id: product.id,
          quantity: 1,
          customization: '',
        },
      ]);
    }
    toast.success('Added to cart');
  };

  const updateQuantity = (productId, quantity) => {
    if (quantity <= 0) {
      setCart(cart.filter((item) => item.product_id !== productId));
    } else {
      setCart(
        cart.map((item) =>
          item.product_id === productId ? { ...item, quantity } : item
        )
      );
    }
  };

  const updateCustomization = (productId, customization) => {
    setCart(
      cart.map((item) =>
        item.product_id === productId ? { ...item, customization } : item
      )
    );
  };

  const getTotal = () => {
    return cart.reduce((total, item) => {
      const product = products.find((p) => p.id === item.product_id);
      return total + (product ? product.price * item.quantity : 0);
    }, 0);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (cart.length === 0) {
      toast.error('Please add items to your cart');
      return;
    }

    if (!customerInfo.customer_name || !customerInfo.customer_phone) {
      toast.error('Please fill in your name and phone number');
      return;
    }

    try {
      setLoading(true);
      const orderData = {
        ...customerInfo,
        items: cart,
        payment_method: paymentMethod,
        notes: notes || undefined,
      };

      const response = await ordersAPI.create(orderData);
      toast.success('Order placed successfully!');
      navigate(`/order/${response.data.id}`);
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to place order');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <h1 className="text-4xl font-bold mb-8">Place Your Order</h1>
      <p className="text-lg text-gray-600 mb-6">
        Order live chickens. We'll kill and dress them fresh for you. You'll be notified via SMS when ready for pickup.
      </p>

      <div className="grid lg:grid-cols-3 gap-8">
        {/* Products */}
        <div className="lg:col-span-2">
          <h2 className="text-2xl font-semibold mb-4">Select Live Chickens</h2>
          <div className="grid md:grid-cols-2 gap-4">
            {products.map((product) => (
              <div key={product.id} className="card">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="text-lg font-semibold">{product.name}</h3>
                  <span className="text-xl font-bold text-primary-600">
                    GHS {product.price.toFixed(2)}
                  </span>
                </div>
                {product.description && (
                  <p className="text-sm text-gray-600 mb-4">{product.description}</p>
                )}
                <button
                  onClick={() => addToCart(product)}
                  className="btn btn-primary w-full"
                  disabled={!product.is_available}
                >
                  {product.is_available ? 'Add to Cart' : 'Unavailable'}
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Cart & Checkout */}
        <div className="lg:col-span-1">
          <div className="card sticky top-4">
            <h2 className="text-2xl font-semibold mb-4">Your Order</h2>

            {cart.length === 0 ? (
              <p className="text-gray-500">Your cart is empty</p>
            ) : (
              <>
                <div className="space-y-4 mb-6">
                  {cart.map((item) => {
                    const product = products.find((p) => p.id === item.product_id);
                    if (!product) return null;
                    return (
                      <div key={item.product_id} className="border-b pb-4">
                        <div className="flex justify-between items-start mb-2">
                          <div>
                            <h4 className="font-semibold">{product.name}</h4>
                            <p className="text-sm text-gray-600">
                              GHS {product.price.toFixed(2)} × {item.quantity}
                            </p>
                          </div>
                          <span className="font-bold">
                            GHS {(product.price * item.quantity).toFixed(2)}
                          </span>
                        </div>
                        <div className="flex items-center space-x-2 mb-2">
                          <button
                            onClick={() => updateQuantity(item.product_id, item.quantity - 1)}
                            className="w-8 h-8 rounded bg-gray-200 hover:bg-gray-300"
                          >
                            -
                          </button>
                          <span className="w-8 text-center">{item.quantity}</span>
                          <button
                            onClick={() => updateQuantity(item.product_id, item.quantity + 1)}
                            className="w-8 h-8 rounded bg-gray-200 hover:bg-gray-300"
                          >
                            +
                          </button>
                        </div>
                <input
                  type="text"
                  placeholder="Special instructions (optional)"
                  value={item.customization}
                  onChange={(e) =>
                    updateCustomization(item.product_id, e.target.value)
                  }
                  className="input text-sm mt-2"
                />
                      </div>
                    );
                  })}
                </div>

                <div className="border-t pt-4 mb-6">
                  <div className="flex justify-between text-xl font-bold">
                    <span>Total:</span>
                    <span className="text-primary-600">GHS {getTotal().toFixed(2)}</span>
                  </div>
                </div>

                <form onSubmit={handleSubmit} className="space-y-4">
                  <div>
                    <label className="label">Name *</label>
                    <input
                      type="text"
                      className="input"
                      value={customerInfo.customer_name}
                      onChange={(e) =>
                        setCustomerInfo({ ...customerInfo, customer_name: e.target.value })
                      }
                      required
                    />
                  </div>
                  <div>
                    <label className="label">Phone *</label>
                    <input
                      type="tel"
                      className="input"
                      value={customerInfo.customer_phone}
                      onChange={(e) =>
                        setCustomerInfo({ ...customerInfo, customer_phone: e.target.value })
                      }
                      required
                    />
                  </div>
                  <div>
                    <label className="label">Email</label>
                    <input
                      type="email"
                      className="input"
                      value={customerInfo.customer_email}
                      onChange={(e) =>
                        setCustomerInfo({ ...customerInfo, customer_email: e.target.value })
                      }
                    />
                  </div>
                  <div>
                    <label className="label">Payment Method</label>
                    <select
                      className="input"
                      value={paymentMethod}
                      onChange={(e) => setPaymentMethod(e.target.value)}
                    >
                      <option value="cash">Cash</option>
                      <option value="mobile_money">Mobile Money</option>
                      <option value="card">Card</option>
                      <option value="hubtel">Hubtel</option>
                      <option value="paystack">Paystack</option>
                    </select>
                  </div>
                  <div>
                    <label className="label">Notes (optional)</label>
                    <textarea
                      className="input"
                      rows="3"
                      value={notes}
                      onChange={(e) => setNotes(e.target.value)}
                      placeholder="Any special instructions..."
                    />
                  </div>
                  <button
                    type="submit"
                    className="btn btn-primary w-full"
                    disabled={loading}
                  >
                    {loading ? 'Placing Order...' : 'Place Order'}
                  </button>
                </form>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Order;

