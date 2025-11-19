# ChickOrder 🐔

A web-based ordering and preparation management system for live chicken sellers. Order live chickens online, and we'll kill and dress them fresh for you. Get notified via SMS when your order is ready for pickup.

## 🌟 Features

- **Live Chicken Ordering**: Order Layer, Broiler, Cockerel, Guinea Fowl, and Saso Layers
- **Fresh Preparation**: We kill and dress chickens fresh when you order
- **Real-time Tracking**: Track your order status from placement to pickup
- **SMS Notifications**: Get notified when your chickens are ready
- **Payment Options**: Cash on Arrival or Mobile Money
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
- **Payments**: Mobile Money (via Hubtel), Cash on Arrival
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
3. **Ready**: Chickens are killed, dressed, and ready for pickup (customer notified via SMS)
4. **Completed**: Customer picks up the order

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
- `GET /admin/sales/today` - Get today's sales statistics with breakdown by product type

Full API documentation available at `http://localhost:8000/docs`

## 🔐 Environment Variables

### Backend (.env)
```env
# Database
DATABASE_URL=sqlite:///./chickorder.db

# JWT Authentication
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Admin Credentials
ADMIN_EMAIL=admin@chickorder.com
ADMIN_PASSWORD=admin123

# Payment Providers (Optional - for production)
HUBTEL_API_KEY=
HUBTEL_CLIENT_ID=
HUBTEL_CLIENT_SECRET=

# Notifications (Optional - for production)
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=
```

### Frontend (.env.local)
```env
VITE_API_URL=http://localhost:8000
```

## 📱 Features in Detail

### Customer Features
- Browse available live chickens with images
- Place orders with special instructions
- Track order status in real-time (Order Placed → Confirmed → Ready → Completed)
- Receive SMS notifications when order is ready
- Payment options: Cash on Arrival or Mobile Money
- View order history and payment status

### Admin Features
- **Dashboard**: View today's sales statistics with breakdown by chicken type
- **Order Management**: Update order status (Confirm → Ready → Completed)
- **Sales Analytics**: Track total chickens sold, revenue, and breakdown by product
- **Payment Tracking**: Monitor payment methods and status
- **SMS Notifications**: Automatically notify customers when orders are ready

## 📊 Dashboard Features

The Admin Dashboard provides:
- **Today's Sales**: Total chickens sold today with breakdown by type (Layer, Broiler, Cockerel, Guinea Fowl, Saso Layers)
- **Revenue Tracking**: Today's revenue and total revenue
- **Order Statistics**: Total, pending, and completed orders
- **Payment Analytics**: Digital payment percentage tracking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

See [LICENSE](LICENSE) file for details.

## 👥 Authors

- Michael Nkema [mykecodes]

## 🙏 Acknowledgments

- Built with FastAPI and React
- Inspired by the need to help my dad's business and digitize chicken ordering processes

## 📞 Support

For issues and questions, please open an issue on the repository.

---

**Made with ❤️ for chicken sellers and customers**

