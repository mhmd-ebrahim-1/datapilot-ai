<div align="center">

# 🧭 DataPilot AI

### Turn Your Data Into Decisions.

AI-powered business intelligence SaaS platform that transforms raw Excel/CSV data into actionable insights, interactive dashboards, forecasts, and executive reports.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Next.js](https://img.shields.io/badge/Next.js-14-black.svg)](https://nextjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg)](https://fastapi.tiangolo.com)

</div>

---

## 📋 Overview

DataPilot AI is a production-grade SaaS platform that allows users and companies to:

- **Upload** Excel/CSV datasets
- **Clean** data automatically with transparent change logs
- **Profile** datasets with comprehensive statistical analysis
- **Score** data quality across multiple dimensions
- **Calculate** KPIs dynamically based on dataset type
- **Visualize** with auto-generated interactive dashboards
- **Generate** AI-powered business insights with supporting metrics
- **Chat** with data using natural language questions
- **Forecast** trends with statistical models
- **Detect** anomalies using statistical methods
- **Report** with professional PDF executive reports
- **Collaborate** with multi-user workspaces and role-based access
- **Scale** with subscription plans and usage limits

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Next.js 14)                     │
│  TypeScript · Tailwind CSS · shadcn/ui · Recharts           │
├─────────────────────────────────────────────────────────────┤
│                  REST API (FastAPI)                          │
│  JWT Auth · Rate Limiting · CORS · OpenAPI                  │
├──────────────┬──────────────┬───────────────────────────────┤
│  PostgreSQL  │    Redis     │   Celery Workers              │
│  (Data)      │ (Cache/Queue)│  (Background Jobs)            │
├──────────────┴──────────────┴───────────────────────────────┤
│              AI Provider (Gemini / OpenAI / Mock)            │
└─────────────────────────────────────────────────────────────┘
```

## 🛠️ Technology Stack

### Frontend
| Technology | Purpose |
|-----------|---------|
| Next.js 14 | React framework (App Router) |
| TypeScript | Type safety |
| Tailwind CSS | Styling |
| shadcn/ui | Component library |
| Recharts | Interactive charts |
| TanStack Query | Server state management |
| React Hook Form + Zod | Form validation |
| Zustand | Client state management |

### Backend
| Technology | Purpose |
|-----------|---------|
| FastAPI | Python web framework |
| SQLAlchemy 2.0 | ORM + database management |
| Alembic | Database migrations |
| Pandas + NumPy | Data processing |
| scikit-learn | ML (anomaly detection, forecasting) |
| Celery + Redis | Background job processing |
| ReportLab | PDF generation |
| Google Generative AI | AI insights (Gemini) |

### Infrastructure
| Technology | Purpose |
|-----------|---------|
| PostgreSQL 15 | Primary database |
| Redis 7 | Cache + message broker |
| Docker | Containerization |
| GitHub Actions | CI/CD |

## 📁 Project Structure

```
datapilot-ai/
├── frontend/                   # Next.js frontend
│   ├── src/
│   │   ├── app/               # App Router pages
│   │   ├── components/        # React components
│   │   ├── lib/               # Utilities, API client
│   │   ├── hooks/             # Custom hooks
│   │   ├── types/             # TypeScript types
│   │   └── locales/           # i18n translations
│   └── public/                # Static assets
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── api/routes/        # API endpoints
│   │   ├── models/            # SQLAlchemy models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── services/          # Business logic
│   │   ├── tasks/             # Celery tasks
│   │   ├── config/            # Configuration
│   │   └── prompts/           # AI prompt templates
│   ├── alembic/               # Database migrations
│   ├── data/                  # Demo datasets
│   ├── tests/                 # Backend tests
│   └── scripts/               # Utility scripts
├── docker-compose.yml          # Multi-service orchestration
├── .env.example               # Environment template
├── .github/workflows/         # CI/CD pipelines
└── docs/                      # Documentation
```

## 🚀 Getting Started

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.11+
- **PostgreSQL** 15+
- **Redis** 7+
- **Docker** (recommended)

### Quick Start with Docker

```bash
# Clone the repository
git clone https://github.com/mhmd-ebrahim-1/datapilot-ai.git
cd datapilot-ai

# Copy environment configuration
cp .env.example .env

# Start all services
docker compose up

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Manual Setup

#### Backend

```bash
cd backend

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Seed demo data
python scripts/seed.py

# Start the server
uvicorn app.main:app --reload --port 8000
```

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

#### Background Workers

```bash
cd backend

# Start Celery worker
celery -A app.tasks.celery_app worker --loglevel=info

# Start Celery beat (for scheduled tasks)
celery -A app.tasks.celery_app beat --loglevel=info
```

## ⚙️ Environment Variables

Copy `.env.example` to `.env` and configure:

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://datapilot:datapilot@localhost:5432/datapilot` |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379/0` |
| `SECRET_KEY` | Application secret key | Required |
| `JWT_SECRET` | JWT signing key | Required |
| `AI_PROVIDER` | AI provider (gemini/openai/mock) | `mock` |
| `AI_API_KEY` | AI provider API key | Required for gemini/openai |
| `AI_MODEL` | AI model name | `gemini-2.0-flash` |
| `STORAGE_PROVIDER` | File storage (local/s3) | `local` |
| `EMAIL_PROVIDER` | Email provider (console/smtp/sendgrid) | `console` |
| `PAYMENT_PROVIDER` | Payment provider (mock/stripe) | `mock` |

See [`.env.example`](.env.example) for the complete list.

## 📡 API Documentation

When the backend is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register new user |
| POST | `/api/v1/auth/login` | Authenticate user |
| POST | `/api/v1/datasets/upload` | Upload dataset |
| GET | `/api/v1/datasets` | List datasets |
| POST | `/api/v1/analyses` | Run analysis |
| GET | `/api/v1/insights/{analysis_id}` | Get AI insights |
| POST | `/api/v1/chat` | Chat with data |
| POST | `/api/v1/forecasts` | Generate forecast |
| POST | `/api/v1/anomalies/detect` | Detect anomalies |
| POST | `/api/v1/reports` | Generate report |
| GET | `/api/v1/billing/usage` | Get usage stats |

## 🤖 AI Configuration

DataPilot AI supports multiple AI providers:

### Google Gemini (Recommended)

```env
AI_PROVIDER=gemini
AI_API_KEY=your-gemini-api-key
AI_MODEL=gemini-2.0-flash
```

### OpenAI

```env
AI_PROVIDER=openai
AI_API_KEY=your-openai-api-key
AI_MODEL=gpt-4o-mini
```

### Mock (Development)

```env
AI_PROVIDER=mock
```

The mock provider returns deterministic responses based on dataset metrics, suitable for development without API costs.

**AI Architecture**: DataPilot AI never sends raw datasets to AI models. Instead:
1. Python/Pandas computes exact metrics and statistics
2. Structured metrics are sent to the AI for reasoning
3. AI responses are validated against source metrics
4. Unsupported claims are rejected

## 🧪 Testing

```bash
# Backend tests
cd backend
python -m pytest tests/ -v

# Frontend build check
cd frontend
npm run build

# Lint
cd frontend && npm run lint
cd backend && python -m ruff check .
```

## 🐳 Docker

```bash
# Start all services
docker compose up

# Start in background
docker compose up -d

# Rebuild after changes
docker compose up --build

# Stop all services
docker compose down

# Reset database
docker compose down -v
```

## 📊 Demo Data

The project includes realistic demo datasets:

| File | Description | Rows |
|------|-------------|------|
| `demo_sales.csv` | Sales transactions with products, regions, customers | 500+ |
| `demo_marketing.csv` | Marketing campaign performance | 200+ |
| `demo_finance.csv` | Financial transactions (income/expenses) | 100+ |
| `demo_hr.csv` | Employee data with departments and performance | 100+ |

## 💳 Subscription Plans

| Feature | Free | Pro ($29/mo) | Business ($99/mo) |
|---------|------|-------------|-------------------|
| Datasets | 5 | 50 | 500 |
| Analyses/month | 10 | 100 | 1,000 |
| AI Requests/month | 20 | 500 | 5,000 |
| Storage | 500 MB | 5 GB | 50 GB |
| AI Chat | ❌ | ✅ | ✅ |
| Forecasting | ❌ | ✅ | ✅ |
| PDF Reports | ❌ | ✅ | ✅ |
| Team Workspaces | ❌ | ❌ | ✅ |
| Scheduled Reports | ❌ | ❌ | ✅ |
| White-label | ❌ | ❌ | ✅ |

## 🔒 Security

- JWT authentication with refresh tokens
- bcrypt password hashing
- Workspace-scoped data isolation
- Server-side file validation (MIME type, extension, size)
- Rate limiting on all endpoints
- CORS restrictions
- Input validation (Pydantic)
- SQL injection prevention (SQLAlchemy parameterized queries)
- No secrets in version control

## 🚢 Deployment

### Recommended Stack

| Service | Provider |
|---------|----------|
| Frontend | Vercel |
| Backend | Railway / Render / Fly.io |
| Database | Managed PostgreSQL (Supabase, Neon, AWS RDS) |
| Redis | Managed Redis (Upstash, AWS ElastiCache) |
| Storage | S3-compatible (AWS S3, Cloudflare R2) |

### Production Checklist

- [ ] Set `DEBUG=false`
- [ ] Configure strong `SECRET_KEY` and `JWT_SECRET`
- [ ] Set `FRONTEND_URL` to production domain
- [ ] Configure HTTPS
- [ ] Set up managed PostgreSQL
- [ ] Set up managed Redis
- [ ] Configure AI provider credentials
- [ ] Set up email provider
- [ ] Configure payment provider (Stripe)
- [ ] Set up file storage (S3)
- [ ] Enable rate limiting
- [ ] Configure CORS for production domain only

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file.

---

<div align="center">

**DataPilot AI** — Turn Your Data Into Decisions.

[Website](http://localhost:3000) · [API Docs](http://localhost:8000/docs) · [Report Bug](https://github.com/mhmd-ebrahim-1/datapilot-ai/issues)

</div>

