import json
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.core.config import get_settings
from app.core.database import engine, Base, AsyncSessionLocal
from app.routes import auth, users, user_likes, people_swipe, matching, chat, discover, contents, payment, legal

settings = get_settings()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables (in production use alembic migrations)
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created/verified")
    except Exception as e:
        logger.warning(f"Could not connect to database on startup: {e}")
        logger.warning("App will start but DB-dependent endpoints will fail")
    yield
    # Shutdown
    try:
        await engine.dispose()
    except Exception:
        pass


app = FastAPI(
    title="VibeLink API",
    description="VibeLink Dating App Backend - Python FastAPI",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/swagger" if settings.environment == "development" else None,
    redoc_url="/redoc" if settings.environment == "development" else None,
)

# CORS
if settings.environment == "development":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    origins = settings.cors_origins.split(",") if settings.cors_origins else ["https://vibelink.app"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Security headers middleware (production only)
if settings.environment != "development":
    @app.middleware("http")
    async def security_headers(request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response

# Register routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(user_likes.router)
app.include_router(people_swipe.router)
app.include_router(matching.router)
app.include_router(chat.router)
app.include_router(discover.router)
app.include_router(contents.router)
app.include_router(payment.router)
app.include_router(legal.router)


# Health check endpoints
@app.get("/health")
async def health():
    checks = []
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
            checks.append({"name": "postgres", "status": "Healthy", "duration": 0})
    except Exception as e:
        checks.append({"name": "postgres", "status": "Unhealthy", "duration": 0})

    overall = "Healthy" if all(c["status"] == "Healthy" for c in checks) else "Unhealthy"
    return {"status": overall, "checks": checks}


@app.get("/health/ready")
async def health_ready():
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
        return {"status": "Healthy"}
    except Exception:
        return JSONResponse(status_code=503, content={"status": "Unhealthy"})


@app.get("/health/live")
async def health_live():
    return {"status": "Healthy"}
