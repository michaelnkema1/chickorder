import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { productsAPI } from '../services/api';
import toast from 'react-hot-toast';
import ProductCard from '../components/ProductCard';

const Products = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [category, setCategory] = useState('');

  useEffect(() => {
    loadProducts();
  }, [category]);

  const loadProducts = async () => {
    try {
      setLoading(true);
      const params = category ? { category } : {};
      const response = await productsAPI.getAll(params);
      setProducts(response.data);
    } catch (error) {
      toast.error('Failed to load products');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  // All products are live chickens, no category filter needed

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center">Loading products...</div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-4">Our Live Chickens</h1>
        <p className="text-gray-600 mb-6">Order live chickens. We kill and dress them fresh for you when you order.</p>
        
        {/* Category Filter - removed since all are live_chicken */}
      </div>

      {products.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500">No products found.</p>
        </div>
      ) : (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {products.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      )}

      <div className="mt-12 text-center">
        <Link to="/order" className="btn btn-primary text-lg px-8 py-3">
          Place Order
        </Link>
      </div>
    </div>
  );
};

export default Products;

