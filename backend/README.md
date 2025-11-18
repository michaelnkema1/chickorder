# ChickOrder Backend API

FastAPI backend for the ChickOrder ordering and preparation management system.

## Features

- **Authentication**: JWT-based authentication for admin and customers
- **Product Management**: CRUD operations for products
- **Order Management**: Order creation, status updates, and tracking
- **Payment Integration**: Hubtel and Paystack payment gateways
- **Notifications**: SMS (Twilio) and WhatsApp notifications
- **Admin Dashboard**: Statistics and order management
- **Order State Machine**: Validated order status transitions

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt (passlib)

## Quick Start

The easiest way to run the backend is using the provided run scripts:

**Linux/Mac:**
```bash
cd backend
./run.sh
```

**Windows:**
```cmd
cd backend
run.bat
```

**Cross-platform (Python):**
```bash
cd backend
python run.py
```

The scripts will automatically:
- Create a virtual environment if it doesn't exist
- Install/update dependencies
- Check and create `.env` file from `.env.example`
- Initialize the database if needed
- Start the FastAPI server

## Setup

### 1. Install Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Database Setup

Create a PostgreSQL database:

```bash
createdb chickorder_db
```

Or using psql:

```sql
CREATE DATABASE chickorder_db;
```

### 3. Environment Configuration

Copy `.env.example` to `.env` and update with your configuration:

```bash
cp .env.example .env
```

Update the following in `.env`:
- `DATABASE_URL`: Your PostgreSQL connection string
- `SECRET_KEY`: A secure random string for JWT
- `ADMIN_EMAIL` and `ADMIN_PASSWORD`: Admin credentials
- Payment provider credentials (Hubtel, Paystack)
- Notification credentials (Twilio, WhatsApp)

### 4. Initialize Database

Run the initialization script to create tables, admin user, and sample products:

```bash
python init_db.py
```

### 5. Run the Server

**Option 1: Using the run script (Recommended)**
```bash
# Linux/Mac
./run.sh

# Windows
run.bat

# Cross-platform
python run.py
```

**Option 2: Manual start**
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

API documentation (Swagger UI): `http://localhost:8000/docs`
Alternative docs (ReDoc): `http://localhost:8000/redoc`

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `GET /auth/me` - Get current user info

### Products
- `GET /products/` - Get all products (public)
- `GET /products/{id}` - Get single product
- `POST /products/` - Create product (admin)
- `PUT /products/{id}` - Update product (admin)
- `DELETE /products/{id}` - Delete product (admin)

### Orders
- `POST /orders/` - Create new order (public)
- `GET /orders/` - Get orders (filtered by user role)
- `GET /orders/{id}` - Get single order
- `PUT /orders/{id}/status` - Update order status (admin)
- `POST /orders/{id}/payment` - Initiate payment

### Admin
- `GET /admin/dashboard` - Get dashboard statistics
- `GET /admin/orders/pending` - Get pending orders

## Order Status Flow

```
PENDING → CONFIRMED → PREPARING → READY → COMPLETED
    ↓         ↓           ↓
CANCELLED  CANCELLED  CANCELLED
```

## Payment Methods

- `cash` - Cash payment
- `mobile_money` - Mobile money
- `card` - Card payment
- `hubtel` - Hubtel payment gateway
- `paystack` - Paystack payment gateway

## Development

### Database Migrations

For production, use Alembic for database migrations:

```bash
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### Testing

Create test files in a `tests/` directory and run with pytest:

```bash
pytest
```

## Production Deployment

1. Set `ENVIRONMENT=production` and `DEBUG=False` in `.env`
2. Use a proper secret key for `SECRET_KEY`
3. Configure CORS origins in `main.py`
4. Use a production ASGI server like Gunicorn with Uvicorn workers
5. Set up proper database backups
6. Configure SSL/TLS certificates

## License

MIT

