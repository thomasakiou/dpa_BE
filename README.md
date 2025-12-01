# DPA Backend - Dynamic People Association

A modern, secure financial association management system built with FastAPI, PostgreSQL, and Domain-Driven Design architecture.

## Features

- 🔐 JWT-based authentication
- 👥 Role-based access control (Admin/Member)
- 💰 Monthly savings tracking
- 📊 Share contributions management
- 💳 Loan applications and repayments
- 📄 PDF statement generation
- 📈 Financial analytics and reports
- 🏗️ Domain-Driven Design architecture

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Authentication**: JWT (python-jose)
- **PDF Generation**: ReportLab

## Project Structure (DDD)

```
dpa_BE/
├── app/
│   ├── domain/              # Domain layer (entities, value objects, events)
│   ├── application/         # Application layer (commands, queries, handlers)
│   ├── infrastructure/      # Infrastructure layer (repositories, database)
│   ├── presentation/        # Presentation layer (API routes, schemas)
│   ├── core/               # Cross-cutting concerns (config, security)
│   └── main.py             # Application entry point
├── alembic/                # Database migrations
├── requirements.txt
└── .env.example
```

## Setup Instructions

### 1. Clone and Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your database credentials and secret key
```

### 3. Setup Database

```bash
# Create PostgreSQL database
createdb dpa_db

# Run migrations
alembic upgrade head

# Initialize with default admin user
python -m app.infrastructure.database.init_db
```

### 4. Run Application

```bash
# Development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 5. Access API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Default Admin Credentials

- **Email**: admin@dpa.com
- **Password**: admin123
- **Member ID**: DPA001

⚠️ **Change these credentials immediately in production!**

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/change-password` - Change password

### Member Endpoints
- `GET /api/v1/members/me` - Get profile
- `GET /api/v1/members/me/dashboard` - Dashboard data
- `GET /api/v1/members/me/statement` - Financial statement
- `GET /api/v1/savings/me` - My savings
- `GET /api/v1/shares/me` - My shares
- `GET /api/v1/loans/me` - My loans

### Admin Endpoints
- `GET /api/v1/admin/dashboard` - Admin analytics
- `GET /api/v1/admin/users` - Manage members
- `GET /api/v1/admin/savings` - Manage savings
- `GET /api/v1/admin/shares` - Manage shares
- `GET /api/v1/admin/loans` - Manage loans
- `GET /api/v1/admin/reports/*` - Financial reports

## Development

### Create New Migration

```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```

### Run Tests

```bash
pytest
```

## License

MIT License
