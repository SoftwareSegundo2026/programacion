from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, FileResponse
from contextlib import asynccontextmanager
from sqlalchemy import text

from app.core.database import engine, Base, AsyncSessionLocal
from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.logging import setup_logging
from app.users.seeder import seed_demo_users

settings = get_settings()
setup_logging(settings.LOG_FILE_PATH, settings.LOG_LEVEL)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Al iniciar el servidor: crea tablas en la BD, agrega columnas extra
    (ImageUrl, IsAdmin), crea usuarios demo. Al cerrar: libera la conexión."""
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

        # Migration: add columns if they don't exist
        migrations = [
            ("Artist", "ImageUrl", "VARCHAR(500)"),
            ("Album", "ImageUrl", "VARCHAR(500)"),
            ("User", "IsAdmin", "BOOLEAN DEFAULT 0"),
        ]
        for table, column, col_type in migrations:
            try:
                await conn.execute(
                    text(f"ALTER TABLE {table} ADD COLUMN {column} {col_type}")
                )
            except Exception:
                pass

        # Set existing admin user as admin
        await conn.execute(
            text('UPDATE "User" SET IsAdmin = 1 WHERE Username = "admin"')
        )

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

# Static files for uploaded images
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def read_root():
    """Página principal con información de la API y links a la documentación."""
    return FileResponse("static/index.html")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return RedirectResponse(url="/static/favicon.svg")
