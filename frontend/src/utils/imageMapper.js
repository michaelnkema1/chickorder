/**
 * Maps product names to their corresponding image paths in the public folder
 */
export const getProductImage = (productName) => {
  const imageMap = {
    'Layer': '/layer.jpeg',
    'Broiler': '/broiler.jpeg',
    'Cockerel': '/cockerel.jpeg',
    'Guinea Fowl': '/guinea-fowl.jpeg',
    'Saso Layers': '/saso-layer.jpeg',
  };

  // Return the mapped image or a default placeholder
  return imageMap[productName] || '/layer.jpeg'; // Default to layer image if not found
};

