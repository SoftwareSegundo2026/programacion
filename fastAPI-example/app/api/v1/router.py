from fastapi import APIRouter
from app.artists.router import router as artists_router
from app.albums.router import router as albums_router
from app.genres.router import router as genres_router

api_router = APIRouter()
api_router.include_router(artists_router, prefix="/artists", tags=["artists"])
api_router.include_router(albums_router, prefix="/albums", tags=["albums"])
api_router.include_router(genres_router, prefix="/genres", tags=["genres"])