# ChickOrder 🐔

A web-based ordering and preparation management system for live chicken sellers. Order live chickens online, and we'll kill and dress them fresh for you. Get notified via SMS when your order is ready for pickup.

## 🌟 Features

- **Live Chicken Ordering**: Order Layer, Broiler, Cockerel, Guinea Fowl, and Saso Layers
- **Fresh Preparation**: We kill and dress chickens fresh when you order
- **Real-time Tracking**: Track your order status from placement to pickup
- **SMS Notifications**: Get notified when your chickens are ready
- **Multiple Payment Options**: Cash, Mobile Money, Card, Hubtel, Paystack
- **Admin Dashboard**: Manage orders, view statistics, and track performance
- **User Authentication**: Secure login and registration system
- **Responsive Design**: Works seamlessly on mobile and desktop

## 🏗️ Architecture

This project consists of two main components:

- **Backend**: FastAPI-based REST API (Python)
- **Frontend**: React-based web application (JavaScript)

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL (optional - SQLite used by default for development)

### 🎯 Easiest Way - Run Everything at Once

**Linux/Mac:**
```bash
./run.sh
```

**Windows:**
```cmd
run.bat
```

**Cross-platform (Python):**
```bash
python run.py
```

This will automatically:
- Set up virtual environments if needed
- Install dependencies
- Initialize the database
- Start both backend and frontend servers

The application will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

**Default Admin Credentials:**
- Email: `admin@chickorder.com`
- Password: `admin123`

### Alternative - Run Separately

#### Backend Setup

```bash
cd backend
./run.sh
# or
python run.py
```

The backend will start at `http://localhost:8000`

#### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend will start at `http://localhost:3000`

## 📁 Project Structure

```
chickorder/
├── backend/                 # FastAPI backend
│   ├── routers/            # API route handlers
│   ├── services/           # Business logic services
│   ├── models.py           # Database models
│   ├── schemas.py          # Pydantic schemas
│   ├── main.py             # FastAPI application
│   └── requirements.txt    # Python dependencies
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # Reusable components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   └── App.jsx         # Main app component
│   └── package.json        # Node dependencies
└── README.md               # This file
```

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI
- **Database**: SQLite (dev) / PostgreSQL (production)
- **ORM**: SQLAlchemy
- **Authentication**: JWT (python-jose)
- **Payments**: Hubtel, Paystack integration
- **Notifications**: Twilio (SMS), WhatsApp Cloud API

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **Styling**: TailwindCSS
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **Notifications**: React Hot Toast

## 📋 Available Products

- **Layer**: GHS 130.00
- **Broiler**: GHS 250.00
- **Cockerel**: GHS 250.00
- **Guinea Fowl**: GHS 250.00
- **Saso Layers**: GHS 200.00

## 🔄 Order Flow

1. **Order Placed**: Customer places order for live chickens
2. **Confirmed**: Order is confirmed, preparation begins
3. **Preparing**: Chickens are being killed and dressed
4. **Ready**: Chickens are dressed and ready for pickup
5. **Completed**: Customer picks up the order

## 📡 API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `GET /auth/me` - Get current user

### Products
- `GET /products/` - Get all products
- `GET /products/{id}` - Get single product
- `POST /products/` - Create product (admin)
- `PUT /products/{id}` - Update product (admin)
- `DELETE /products/{id}` - Delete product (admin)

### Orders
- `POST /orders/` - Create new order
- `GET /orders/` - Get orders (filtered by user role)
- `GET /orders/{id}` - Get single order
- `PUT /orders/{id}/status` - Update order status (admin)
- `POST /orders/{id}/payment` - Initiate payment

### Admin
- `GET /admin/dashboard` - Get dashboard statistics
- `GET /admin/orders/pending` - Get pending orders

Full API documentation available at `http://localhost:8000/docs`

## 🔐 Environment Variables

### Backend (.env)
```env
DATABASE_URL=sqlite:///./chickorder.db
SECRET_KEY=your-secret-key
ADMIN_EMAIL=admin@chickorder.com
ADMIN_PASSWORD=admin123
# Payment and notification credentials...
```

### Frontend (.env.local)
```env
VITE_API_URL=http://localhost:8000
```

## 📱 Features in Detail

### Customer Features
- Browse available live chickens
- Place orders with special instructions
- Track order status in real-time
- Receive SMS notifications
- Multiple payment options
- Order history

### Admin Features
- Dashboard with key metrics
- Order management and status updates
- Product management (CRUD)
- Customer order tracking
- Payment status monitoring
- Performance analytics

## 🎯 MVP Success Metrics

- ✅ Reduce average wait time by 50%
- ✅ Decrease phone call orders by 70%
- ✅ Customer satisfaction > 4.5/5
- ✅ 60% digital payments

## 🚀 Deployment

### Backend
1. Set `ENVIRONMENT=production` in `.env`
2. Use PostgreSQL for production database
3. Configure proper CORS origins
4. Set up SSL/TLS certificates
5. Use production ASGI server (Gunicorn + Uvicorn)

### Frontend
1. Build: `npm run build`
2. Serve static files with Nginx or similar
3. Configure API URL for production
4. Set up HTTPS

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

See [LICENSE](LICENSE) file for details.

## 👥 Authors

- ChickOrder Development Team

## 🙏 Acknowledgments

- Built with FastAPI and React
- Inspired by the need to digitize chicken ordering processes

## 📞 Support

For issues and questions, please open an issue on the repository.

---

**Made with ❤️ for chicken sellers and customers**

