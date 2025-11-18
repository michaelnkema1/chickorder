import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Hero Section */}
      <div className="text-center mb-16">
        <h1 className="text-5xl font-bold text-gray-900 mb-4">
          Welcome to ChickOrder 🐔
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Order live chickens online. We kill and dress them fresh for you. Get notified when ready for pickup!
        </p>
        <div className="flex justify-center space-x-4">
          <Link to="/products" className="btn btn-primary text-lg px-8 py-3">
            Browse Menu
          </Link>
          <Link to="/order" className="btn btn-outline text-lg px-8 py-3">
            Place Order
          </Link>
        </div>
      </div>

      {/* Features */}
      <div className="grid md:grid-cols-3 gap-8 mb-16">
        <div className="card text-center">
          <div className="text-4xl mb-4">🐔</div>
          <h3 className="text-xl font-semibold mb-2">Fresh Live Chickens</h3>
          <p className="text-gray-600">
            Order live chickens. We kill and dress them fresh when you order.
          </p>
        </div>
        <div className="card text-center">
          <div className="text-4xl mb-4">📱</div>
          <h3 className="text-xl font-semibold mb-2">Easy Payment</h3>
          <p className="text-gray-600">
            Pay securely with mobile money, cards, or cash on pickup.
          </p>
        </div>
        <div className="card text-center">
          <div className="text-4xl mb-4">🔔</div>
          <h3 className="text-xl font-semibold mb-2">SMS Notifications</h3>
          <p className="text-gray-600">
            Get notified via SMS when your chicken is dressed and ready for pickup.
          </p>
        </div>
      </div>

      {/* How It Works */}
      <div className="card">
        <h2 className="text-3xl font-bold mb-8 text-center">How It Works</h2>
        <div className="grid md:grid-cols-4 gap-6">
          <div className="text-center">
            <div className="bg-primary-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl font-bold text-primary-600">1</span>
            </div>
            <h4 className="font-semibold mb-2">Browse & Order</h4>
            <p className="text-sm text-gray-600">Choose from our live chicken options</p>
          </div>
          <div className="text-center">
            <div className="bg-primary-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl font-bold text-primary-600">2</span>
            </div>
            <h4 className="font-semibold mb-2">We Prepare</h4>
            <p className="text-sm text-gray-600">We kill and dress your chicken fresh</p>
          </div>
          <div className="text-center">
            <div className="bg-primary-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl font-bold text-primary-600">3</span>
            </div>
            <h4 className="font-semibold mb-2">Get Notified</h4>
            <p className="text-sm text-gray-600">Receive SMS when your order is ready</p>
          </div>
          <div className="text-center">
            <div className="bg-primary-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl font-bold text-primary-600">4</span>
            </div>
            <h4 className="font-semibold mb-2">Pickup</h4>
            <p className="text-sm text-gray-600">Collect your fresh dressed chicken</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;

