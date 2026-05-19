from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.database import engine, Base, AsyncSessionLocal
from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.logging import setup_logging
from app.auth.seeder import seed_demo_users

settings = get_settings()
setup_logging(settings.LOG_FILE_PATH, settings.LOG_LEVEL)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    async with engine.begin() as conn:
        # Create tables if they don't exist
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        await seed_demo_users(session)
    yield
    # Shutdown
    await engine.dispose()

app = FastAPI(
    title="FastAPI Example",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def read_root():
    return {"message": "Hello from fastapi-example!"}
