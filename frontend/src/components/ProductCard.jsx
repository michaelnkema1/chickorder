import { getProductImage } from '../utils/imageMapper';

const ProductCard = ({ product }) => {
  const imagePath = getProductImage(product.name);

  return (
    <div className="card hover:shadow-lg transition-shadow">
      <img
        src={imagePath}
        alt={product.name}
        className="w-full h-48 object-cover rounded-lg mb-4"
        onError={(e) => {
          // Fallback to a placeholder if image fails to load
          e.target.src = '/layer.jpeg';
        }}
      />
      <div className="flex justify-between items-start mb-2">
        <h3 className="text-xl font-semibold">{product.name}</h3>
        <span className="text-2xl font-bold text-primary-600">
          GHS {product.price.toFixed(2)}
        </span>
      </div>
      {product.description && (
        <p className="text-gray-600 mb-4">{product.description}</p>
      )}
      <div className="flex items-center justify-between">
        <span className={`px-3 py-1 rounded-full text-sm ${
          product.is_available
            ? 'bg-green-100 text-green-800'
            : 'bg-red-100 text-red-800'
        }`}>
          {product.is_available ? 'Available' : 'Unavailable'}
        </span>
        {product.category && (
          <span className="text-sm text-gray-500 capitalize">
            {product.category}
          </span>
        )}
      </div>
    </div>
  );
};

export default ProductCard;

