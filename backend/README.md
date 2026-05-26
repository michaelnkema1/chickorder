# ChickOrder Backend API

FastAPI backend for the ChickOrder ordering and preparation management system.

## Tech Stack

| Component | Library/Service |
|---|---|
| Framework | FastAPI |
| Database | Supabase (hosted PostgreSQL) |
| ORM | SQLAlchemy 2.0 |
| Auth | JWT via `python-jose` |
| Password hashing | `passlib[bcrypt]` |
| SMS | Twilio |
| Payments | Hubtel, Paystack |

## Local Setup

### 1. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure environment variables

Edit `backend/.env`:

```env
# Supabase Session Pooler URL (port 5432)
# Find it at: Supabase → Project Settings → Database → Connection Pooling → Session Mode
# IMPORTANT: Use the Session Pooler host (*.pooler.supabase.com), NOT the direct connection
# host (db.*.supabase.co) — the direct host is IPv6-only and unreachable on many networks.
DATABASE_URL=postgresql://postgres.[project-ref]:[password]@aws-0-[region].pooler.supabase.com:5432/postgres

SECRET_KEY=your-random-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

ADMIN_EMAIL=admin@chickorder.com
ADMIN_PASSWORD=admin123

ENVIRONMENT=development
DEBUG=True
```

> **Password with special characters?** URL-encode them:  
> `@` → `%40` · `=` → `%3D` · `#` → `%23` · `?` → `%3F`  
> Example: password `pass@word` becomes `pass%40word` in the URL.

### 3. Initialize the database

Creates all tables and seeds the admin user + sample products:

```bash
python3 init_db.py
```

This is **idempotent** — safe to run multiple times without duplicating data.

### 4. Start the server

```bash
uvicorn main:app --reload
```

- API: http://localhost:8000
- Swagger docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /auth/register` — Register new user
- `POST /auth/login` — Login, returns JWT bearer token
- `GET /auth/me` — Get current authenticated user

### Products
- `GET /products/` — List all available products (public)
- `GET /products/{id}` — Get single product (public)
- `POST /products/` — Create product (admin only)
- `PUT /products/{id}` — Update product (admin only)
- `DELETE /products/{id}` — Delete product (admin only)

### Orders
- `POST /orders/` — Create new order (public)
- `GET /orders/` — List orders (scoped by role)
- `GET /orders/{id}` — Get single order
- `PUT /orders/{id}/status` — Update order status (admin only)
- `POST /orders/{id}/payment` — Initiate payment

### Admin
- `GET /admin/dashboard` — Dashboard stats (admin only)
- `GET /admin/orders/pending` — Pending orders (admin only)
- `GET /admin/sales/today` — Today's sales (admin only)

## Order Status Flow

```
PENDING → CONFIRMED → READY → COMPLETED
   ↓          ↓         ↓
CANCELLED  CANCELLED  CANCELLED
```

## Payment Methods

| Method | Key |
|---|---|
| Cash on Arrival | `cash` |
| Mobile Money | `mobile_money` |
| Card | `card` |
| Hubtel | `hubtel` |
| Paystack | `paystack` |

## Production Deployment (Render)

The backend deploys as a Docker container on Render. On startup, `start.sh` runs:

1. `python3 init_db.py` — creates tables + seeds data (idempotent)
2. `uvicorn main:app ...` — starts the server

### Required Render environment variables

Set these manually in the Render dashboard for the `chickorder-backend` service:

| Key | Value |
|---|---|
| `DATABASE_URL` | Supabase Session Pooler connection string |

All other variables (`SECRET_KEY`, `ADMIN_EMAIL`, etc.) are defined in `render.yaml`.

### CORS

In production, the backend allows requests **only** from the URL in `FRONTEND_URL`.  
This is set to `https://chickorder-frontend.onrender.com` in `render.yaml`.  
Update it there if you deploy the frontend to a different host.

## Project Structure

```
backend/
├── routers/
│   ├── auth.py        # /auth endpoints
│   ├── products.py    # /products endpoints
│   ├── orders.py      # /orders endpoints
│   ├── admin.py       # /admin endpoints
│   └── payments.py    # /orders/{id}/payment
├── services/          # Business logic helpers
├── models.py          # SQLAlchemy models (User, Product, Order, etc.)
├── schemas.py         # Pydantic request/response models
├── database.py        # Engine + session factory (pool_pre_ping enabled)
├── config.py          # Pydantic Settings (loaded from .env)
├── auth.py            # JWT helpers, password hashing, auth dependencies
├── init_db.py         # Table creation + data seeding script
├── start.sh           # Docker container entrypoint
├── main.py            # FastAPI app + CORS middleware
├── requirements.txt
└── Dockerfile
```

## License

MIT
