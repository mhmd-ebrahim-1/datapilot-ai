from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import auth, workspaces, datasets, analyses, insights, chat, forecasts, anomalies, reports, billing, users, admin
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
import os
from app.config.settings import settings

app = FastAPI(title="DataPilot AI", version="1.0.0")
# Ensure upload/storage directory exists
os.makedirs(settings.STORAGE_PATH, exist_ok=True)

# Create database tables if not existing
Base.metadata.create_all(bind=engine)

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

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(workspaces.router, prefix="/api/v1/workspaces", tags=["workspaces"])
app.include_router(datasets.router, prefix="/api/v1/datasets", tags=["datasets"])
app.include_router(analyses.router, tags=["analyses"])
app.include_router(insights.router, tags=["insights"])
app.include_router(chat.router, tags=["chat"])
app.include_router(forecasts.router, tags=["forecasts"])
app.include_router(anomalies.router, tags=["anomalies"])
app.include_router(reports.router, tags=["reports"])
app.include_router(billing.router, tags=["billing"])
app.include_router(users.router, tags=["users"])
app.include_router(admin.router, tags=["admin"])
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

@app.get("/health")
@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
    return {"status": "ok", "app": settings.APP_NAME, "environment": settings.APP_ENV}
