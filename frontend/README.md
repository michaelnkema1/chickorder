# ChickOrder Frontend

React frontend for the ChickOrder ordering and preparation management system.

## Tech Stack

- **Framework**: React 18
- **Build Tool**: Vite
- **Styling**: TailwindCSS
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **Notifications**: React Hot Toast

## Features

- 🛍️ **Product Catalog**: Browse available chicken products
- 🛒 **Order Management**: Add items to cart, customize, and place orders
- 📱 **Order Tracking**: Real-time order status updates
- 👤 **User Authentication**: Register and login
- 🔐 **Admin Dashboard**: Manage orders and view statistics
- 💳 **Payment Integration**: Support for multiple payment methods
- 📱 **Responsive Design**: Works on mobile and desktop

## Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Environment Configuration

Create a `.env` file (optional, defaults to localhost:8000):

```env
VITE_API_URL=http://localhost:8000
```

### 3. Run Development Server

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

## Project Structure

```
frontend/
├── src/
│   ├── components/      # Reusable components
│   │   ├── Navbar.jsx
│   │   ├── ProductCard.jsx
│   │   └── ProtectedRoute.jsx
│   ├── pages/           # Page components
│   │   ├── Home.jsx
│   │   ├── Products.jsx
│   │   ├── Order.jsx
│   │   ├── OrderTracking.jsx
│   │   ├── Login.jsx
│   │   ├── Register.jsx
│   │   ├── AdminDashboard.jsx
│   │   └── AdminOrders.jsx
│   ├── services/        # API services
│   │   └── api.js
│   ├── App.jsx          # Main app component
│   ├── main.jsx         # Entry point
│   └── index.css        # Global styles
├── index.html
├── package.json
├── vite.config.js
└── tailwind.config.js
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## API Integration

The frontend communicates with the backend API at `http://localhost:8000`. All API calls are handled through the `services/api.js` file.

## Authentication

- Users can register and login
- JWT tokens are stored in localStorage
- Protected routes require authentication
- Admin routes require admin privileges

## Admin Access

Default admin credentials:
- Email: `admin@chickorder.com`
- Password: `admin123`

## License

MIT

