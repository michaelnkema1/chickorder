# ChickOrder 🐔

A web-based ordering and preparation management system for live chicken sellers. Order live chickens online, and we'll kill and dress them fresh for you — get notified via SMS when your order is ready for pickup.

## 🚀 Live Deployment

| Service | URL |
|---|---|
| Frontend | https://chickorder-frontend.onrender.com |
| Backend API | https://chickorder-backend.onrender.com |
| API Docs (Swagger) | https://chickorder-backend.onrender.com/docs |

## 🌟 Features

- **Live Chicken Ordering** — Layer, Broiler, Cockerel, Guinea Fowl, Saso Layers
- **Fresh Preparation** — Chickens are killed and dressed fresh per order
- **Order Tracking** — Real-time status from placement to pickup
- **SMS Notifications** — Powered by Twilio
- **Payment Options** — Cash on Arrival, Mobile Money, Hubtel, Paystack
- **Admin Dashboard** — Order management, daily sales, and performance stats
- **JWT Authentication** — Secure admin and customer login
- **Responsive Design** — Mobile and desktop friendly

## 🏗️ Architecture

| Layer | Technology |
|---|---|
| Backend | FastAPI (Python 3.10) |
| Frontend | React 18 + Vite |
| Database | Supabase (hosted PostgreSQL) |
| ORM | SQLAlchemy 2.0 |
| Deployment | Docker + Render.com |

## 🖥️ Local Development

### Prerequisites

- Python 3.10+
- Node.js 18+
- A [Supabase](https://supabase.com) project (free tier works)

### 1. Clone the repo

```bash
git clone https://github.com/michaelnkema1/chickorder.git
cd chickorder
```

### 2. Backend setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Copy `.env` and fill in your Supabase connection string:

```bash
# backend/.env
DATABASE_URL=postgresql://postgres.[project-ref]:[password]@aws-0-[region].pooler.supabase.com:5432/postgres
SECRET_KEY=your-random-secret-key
ADMIN_EMAIL=admin@chickorder.com
ADMIN_PASSWORD=admin123
```

> **Important:** Use the **Session Pooler** URL from Supabase (port `5432`, host `*.pooler.supabase.com`).  
> The direct connection host (`db.*.supabase.co`) is IPv6-only and may not be reachable from all networks.  
> Find it at: **Supabase Dashboard → Project Settings → Database → Connection Pooling → Session Mode**

Initialize the database (creates tables + seeds admin user and sample products):

```bash
python3 init_db.py
```

Start the API server:

```bash
uvicorn main:app --reload
# API available at http://localhost:8000
# Docs at http://localhost:8000/docs
```

### 3. Frontend setup

```bash
cd frontend
npm install
npm run dev
# App available at http://localhost:5173
```

### Quick Start (both services)

```bash
./run.sh
```

## ☁️ Production Deployment (Render)

The project deploys automatically from `render.yaml` on every push to `main`.

### Environment variables to set manually in the Render dashboard

| Variable | Where to set | Value |
|---|---|---|
| `DATABASE_URL` | `chickorder-backend` service | Supabase Session Pooler URL |

All other variables are defined in `render.yaml` (auto-generated `SECRET_KEY`, `ADMIN_EMAIL`, etc.).

> **CORS** — The backend is configured to allow requests only from `https://chickorder-frontend.onrender.com` in production. Update `FRONTEND_URL` in `render.yaml` if you deploy the frontend elsewhere.

### Deployment flow on Render

On each deploy, `start.sh` runs automatically:
1. Creates all database tables via SQLAlchemy (`Base.metadata.create_all`)
2. Seeds the admin user and sample products (idempotent — safe to re-run)
3. Starts the Uvicorn server

## 📁 Project Structure

```
chickorder/
├── backend/                 # FastAPI backend
│   ├── routers/             # API route handlers (auth, products, orders, admin, payments)
│   ├── services/            # Business logic
│   ├── models.py            # SQLAlchemy database models
│   ├── schemas.py           # Pydantic request/response schemas
│   ├── database.py          # DB engine + session (Supabase PostgreSQL)
│   ├── config.py            # Settings loaded from environment variables
│   ├── init_db.py           # DB initializer — creates tables + seeds data
│   ├── start.sh             # Docker entrypoint (seed + start server)
│   ├── .env                 # Local dev environment variables (not committed)
│   ├── .env.production      # Production env reference (not committed)
│   └── Dockerfile
├── frontend/                # React + Vite frontend
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/           # Page-level components
│   │   └── services/api.js  # Axios API client
│   ├── .env                 # Local dev (VITE_API_URL=http://localhost:8000)
│   ├── .env.production      # Production (VITE_API_URL=https://chickorder-backend.onrender.com)
│   └── Dockerfile
├── docker-compose.yml       # Local Docker setup
├── render.yaml              # Render.com deployment config
└── README.md
```

## 🔐 Default Admin Credentials

| Field | Value |
|---|---|
| Email | `admin@chickorder.com` |
| Password | `admin123` |

> Change these after first login in production.

## 📡 API Endpoints

### Authentication
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/auth/register` | Public | Register new user |
| POST | `/auth/login` | Public | Login, returns JWT token |
| GET | `/auth/me` | User | Get current user info |

### Products
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/products/` | Public | List all available products |
| GET | `/products/{id}` | Public | Get a single product |
| POST | `/products/` | Admin | Create product |
| PUT | `/products/{id}` | Admin | Update product |
| DELETE | `/products/{id}` | Admin | Delete product |

### Orders
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/orders/` | Public | Create new order |
| GET | `/orders/` | User/Admin | List orders |
| GET | `/orders/{id}` | User/Admin | Get single order |
| PUT | `/orders/{id}/status` | Admin | Update order status |
| POST | `/orders/{id}/payment` | User | Initiate payment |

### Admin
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/admin/dashboard` | Admin | Dashboard statistics |
| GET | `/admin/orders/pending` | Admin | Pending orders |
| GET | `/admin/sales/today` | Admin | Today's sales |

## 📦 Products (Default Seed Data)

| Name | Price (GHS) | Category |
|---|---|---|
| Layer | 130.00 | live_chicken |
| Broiler | 250.00 | live_chicken |
| Cockerel | 250.00 | live_chicken |
| Guinea Fowl | 250.00 | live_chicken |
| Saso Layers | 200.00 | live_chicken |

## 📝 License

See [LICENSE](LICENSE) file for details.

## 👤 Author

**Michael Nkema** — [@mykecodes](https://github.com/michaelnkema1)

---

*Built with ❤️ to digitize chicken ordering for my dad's business.*
