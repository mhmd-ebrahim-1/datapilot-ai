import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
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
from app.config.database import engine, Base
from app.config.settings import settings

# Ensure upload/storage directory exists
os.makedirs(settings.STORAGE_PATH, exist_ok=True)

# Create database tables if not existing
Base.metadata.create_all(bind=engine)

# Ensure newly added SQLite columns exist without requiring manual migration
if settings.DATABASE_URL.startswith("sqlite"):
    try:
        with engine.connect() as conn:
            # Check error_message column in datasets table
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
def health():
    return {"status": "ok", "app": settings.APP_NAME, "environment": settings.APP_ENV}
