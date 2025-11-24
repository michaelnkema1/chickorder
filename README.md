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

## 🚀 Quick Deploy to Render.com (Free)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

**Quick Steps:**
1. Push your code to GitHub
2. Sign up at [Render.com](https://render.com)
3. Click "New +" → "Blueprint"
4. Connect your repo - Render detects `render.yaml`
5. Click "Apply"
6. Wait ~5 minutes for deployment

**Detailed Guide**: See [docs/RENDER_DEPLOYMENT.md](docs/RENDER_DEPLOYMENT.md)

Your app will be live at:
- Frontend: `https://chickorder-frontend.onrender.com`
- Backend API: `https://chickorder-backend.onrender.com`
- API Docs: `https://chickorder-backend.onrender.com/docs`

## 🏗️ Architecture

- **Backend**: FastAPI (Python)
- **Frontend**: React + Vite
- **Database**: PostgreSQL
- **Deployment**: Docker + Render.com

## 🖥️ Local Development

### Prerequisites

- Python 3.10+
- Node.js 18+
- Docker & Docker Compose (for Docker setup)

### Option 1: Docker (Recommended)

```bash
# Start all services with Docker
docker-compose up -d

# Initialize database
docker exec -it chickorder-backend python init_db.py
```

Access at:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 2: Manual Setup

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python init_db.py
python run.py
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

**Quick Start Script:**
```bash
./run.sh  # Runs both backend and frontend
```

## 📁 Project Structure

```
chickorder/
├── backend/                 # FastAPI backend
│   ├── routers/            # API endpoints
│   ├── services/           # Business logic
│   ├── models.py           # Database models
│   ├── schemas.py          # Pydantic schemas
│   └── Dockerfile          # Backend Docker config
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   └── services/       # API client
│   └── Dockerfile          # Frontend Docker config
├── docs/                   # Documentation
│   └── RENDER_DEPLOYMENT.md
├── docker-compose.yml      # Local Docker setup
├── render.yaml             # Render.com deployment config
└── README.md               # This file
```

## 🔐 Default Credentials

- Email: `admin@chickorder.com`
- Password: `admin123`

⚠️ **IMPORTANT**: Change the admin password immediately after deployment!

## 📡 API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `GET /auth/me` - Get current user

### Products
- `GET /products/` - Get all products
- `POST /products/` - Create product (admin)

### Orders
- `POST /orders/` - Create order
- `GET /orders/` - Get orders
- `PUT /orders/{id}/status` - Update status (admin)

Full documentation: http://localhost:8000/docs

## 🛠️ Tech Stack

### Backend
- FastAPI
- SQLAlchemy + PostgreSQL
- JWT Authentication
- Twilio (SMS)
- Hubtel/Paystack (Payments)

### Frontend
- React 18
- Vite
- TailwindCSS
- React Router v6
- Axios

## 🆓 Render Free Tier

- PostgreSQL: Free for 90 days
- Backend: Free (sleeps after 15min inactivity)
- Frontend: Free (always on)
- Automatic SSL
- Auto-deploy from Git

**Note**: Backend may take 30 seconds to wake up from sleep.

## 📝 License

See [LICENSE](LICENSE) file for details.

## 👥 Author

Michael Nkema [@mykecodes]

## 🙏 Acknowledgments

Built with ❤️ to digitize chicken ordering for my dad's business.

---

**Made with ❤️ for chicken sellers and customers**
