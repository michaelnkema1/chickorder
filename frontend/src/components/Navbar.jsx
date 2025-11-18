import { Link } from 'react-router-dom';

const Navbar = ({ user, onLogout }) => {
  return (
    <nav className="bg-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="text-2xl font-bold text-primary-600">
              🐔 ChickOrder
            </Link>
          </div>
          <div className="flex items-center space-x-4">
            <Link
              to="/products"
              className="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium"
            >
              Products
            </Link>
            <Link
              to="/order"
              className="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium"
            >
              Order
            </Link>
            {user ? (
              <>
                {user.is_admin && (
                  <Link
                    to="/admin"
                    className="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium"
                  >
                    Admin
                  </Link>
                )}
                <span className="text-gray-700 px-3 py-2 text-sm">
                  {user.name}
                </span>
                <button
                  onClick={onLogout}
                  className="btn btn-outline text-sm"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link
                  to="/login"
                  className="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium"
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  className="btn btn-primary text-sm"
                >
                  Register
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;

