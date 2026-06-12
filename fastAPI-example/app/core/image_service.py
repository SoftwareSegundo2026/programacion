import os
from pathlib import Path
from fastapi import UploadFile, HTTPException
from fastapi.responses import FileResponse, RedirectResponse
from app.core.config import get_settings

settings = get_settings()

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}


def _get_storage_dir(entity_type: str) -> Path:
    """Devuelve la carpeta donde se guardan las imágenes (artists/ o albums/), creándola si no existe."""
    upload_dir = Path(settings.UPLOAD_DIR) / entity_type
    upload_dir.mkdir(parents=True, exist_ok=True)
    return upload_dir


def _find_existing(entity_type: str, entity_id: int) -> Path | None:
    """Busca si ya existe una imagen para esta entidad (sin importar la extensión)."""
    storage_dir = _get_storage_dir(entity_type)
    for ext in ALLOWED_EXTENSIONS:
        path = storage_dir / f"{entity_id}{ext}"
        if path.exists():
            return path
    return None


def _remove_existing(entity_type: str, entity_id: int):
    """Elimina cualquier imagen existente de la entidad (para reemplazarla)."""
    existing = _find_existing(entity_type, entity_id)
    if existing:
        existing.unlink()


def _to_url_path(absolute_path: Path) -> str:
    """Convierte una ruta de archivo en una URL accesible (ej: /static/images/artists/5.jpg)."""
    static_root = Path(settings.UPLOAD_DIR).resolve()
    return f"/static/images/{absolute_path.parent.name}/{absolute_path.name}"


async def save_upload(entity_type: str, entity_id: int, file: UploadFile) -> str:
    """Guarda una imagen subida por el usuario y devuelve su URL."""
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid image format: {ext}. Allowed: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    _remove_existing(entity_type, entity_id)
    storage_dir = _get_storage_dir(entity_type)
    dest = storage_dir / f"{entity_id}{ext}"

    content = await file.read()
    dest.write_bytes(content)

    return _to_url_path(dest)


DEFAULT_IMAGES = {
    "artists": "static/images/default-artist.svg",
    "albums": "static/images/default-album.svg",
}


def get_image_response(image_url: str | None, entity_type: str = "artists"):
    """Devuelve la imagen: si es local la entrega como archivo, si es externa redirige,
    si no hay imagen muestra un placeholder SVG por defecto."""
    if image_url and image_url.startswith("/static/"):
        file_path = Path(".") / image_url.lstrip("/")
        file_path = file_path.resolve()
        if file_path.exists():
            return FileResponse(str(file_path))

    if image_url and not image_url.startswith("/static/"):
        return RedirectResponse(url=image_url)

    default = DEFAULT_IMAGES.get(entity_type, "static/images/default-artist.svg")
    return FileResponse(default, media_type="image/svg+xml")


async def fetch_from_wikipedia(entity_type: str, entity_id: int, query: str) -> str:
    """Busca en Wikipedia una imagen del artista/álbum, la descarga y la guarda localmente."""
    import httpx

    search_url = "https://en.wikipedia.org/w/api.php"

    async with httpx.AsyncClient(timeout=15) as client:
        search_params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
            "srlimit": 1,
        }
        search_headers = {
            "User-Agent": "FastAPI-Example/1.0 (https://github.com/example/fastapi-example; example@example.com)"
        }
        search_resp = await client.get(
            search_url, params=search_params, headers=search_headers
        )
        if search_resp.status_code == 403:
            raise HTTPException(
                status_code=503,
                detail="Wikipedia API is not available (rate limited). Try uploading the image manually.",
            )
        search_resp.raise_for_status()
        search_data = search_resp.json()

        search_results = search_data.get("query", {}).get("search", [])
        if not search_results:
            raise HTTPException(
                status_code=404,
                detail=f"No Wikipedia page found for '{query}'",
            )

        page_title = search_results[0]["title"]

        image_params = {
            "action": "query",
            "titles": page_title,
            "prop": "pageimages",
            "format": "json",
            "pithumbsize": 500,
        }
        img_resp = await client.get(
            search_url, params=image_params, headers=search_headers
        )
        img_resp.raise_for_status()
        img_data = img_resp.json()

        pages = img_data.get("query", {}).get("pages", {})
        thumbnail = None
        for page in pages.values():
            thumbnail = page.get("thumbnail")
            break

        if not thumbnail or "source" not in thumbnail:
            raise HTTPException(
                status_code=404,
                detail=f"No image found on Wikipedia page '{page_title}'",
            )

        image_source = thumbnail["source"]

        download_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:120.0) Gecko/20100101 Firefox/120.0",
            "Referer": "https://en.wikipedia.org/",
        }
        download_resp = await client.get(
            image_source, headers=download_headers, follow_redirects=True
        )
        if download_resp.status_code == 403:
            raise HTTPException(
                status_code=503,
                detail="Wikipedia image server is not available. Try uploading the image manually.",
            )
        download_resp.raise_for_status()

        content_type = download_resp.headers.get("content-type", "image/jpeg")
        ext_map = {
            "image/jpeg": ".jpg",
            "image/png": ".png",
            "image/gif": ".gif",
            "image/webp": ".webp",
        }
        ext = ext_map.get(content_type, ".jpg")

        _remove_existing(entity_type, entity_id)
        storage_dir = _get_storage_dir(entity_type)
        dest = storage_dir / f"{entity_id}{ext}"
        dest.write_bytes(download_resp.content)

        return _to_url_path(dest)
