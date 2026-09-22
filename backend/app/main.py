import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.api.routes import (
    auth,
    workspaces,
    datasets,
    analyses,
    insights,
    chat,
    forecasts,
    anomalies,
    reports,
    billing,
    users,
    admin
)
from app.config.database import engine, Base, get_db
from app.config.settings import settings

# Ensure upload/storage directory exists
os.makedirs(settings.STORAGE_PATH, exist_ok=True)

# Create database tables if not existing
Base.metadata.create_all(bind=engine)

# Ensure newly added SQLite columns exist without requiring manual migration
if settings.DATABASE_URL.startswith("sqlite"):
    try:
        with engine.connect() as conn:
            result = conn.execute(text("PRAGMA table_info(datasets);")).fetchall()
            col_names = [row[1] for row in result]
            if "error_message" not in col_names:
                conn.execute(text("ALTER TABLE datasets ADD COLUMN error_message VARCHAR;"))
                conn.commit()
    except Exception:
        pass

app = FastAPI(
    title="DataPilot AI API",
    description="Turn Your Data Into Decisions — Business Intelligence & Automated Analytics SaaS Engine",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Explicit allowed origins for CORS security in production
allowed_origins = settings.cors_origin_list
if not allowed_origins:
    allowed_origins = ["http://localhost:3000", "http://127.0.0.1:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=r"^https:\/\/.*(\.vercel\.app|\.koyeb\.app)$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all 12 API Routers
app.include_router(auth.router)
app.include_router(workspaces.router)
app.include_router(datasets.router)
app.include_router(analyses.router)
app.include_router(insights.router)
app.include_router(chat.router)
app.include_router(forecasts.router)
app.include_router(anomalies.router)
app.include_router(reports.router)
app.include_router(billing.router)
app.include_router(users.router)
app.include_router(admin.router)

@app.get("/health", tags=["Health"])
def health(db: Session = Depends(get_db)):
    db_status = "healthy"
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        db_status = "unhealthy"
        
    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "app": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "database": db_status
    }
