from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.database import engine, Base
from app.api.v1.router import api_router
from app.core.config import get_settings

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    # from sqlalchemy import create_engine
    # sync_engine = create_engine(settings.DATABASE_URL.replace('sqlite+aiosqlite://', 'sqlite://'))
    # Base.metadata.create_all(bind=sync_engine)
    # sync_engine.dispose()
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
