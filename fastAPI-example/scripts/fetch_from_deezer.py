"""
Fetch artist photos and album covers from the Deezer API (free, no key required).
Runs on items that still lack an ImageUrl.
"""
import asyncio, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.database import AsyncSessionLocal
from app.artists.model import Artist
from app.albums.model import Album
from sqlalchemy import select
import httpx


async def fetch_image(entity_type: str, entity_id: int, query: str) -> str | None:
    """Search Deezer for an artist image or album cover."""
    storage_dir = Path("./static/images") / entity_type
    storage_dir.mkdir(parents=True, exist_ok=True)

    endpoint = "artist" if entity_type == "artists" else "album"
    url = f"https://api.deezer.com/search/{endpoint}?q={query}&limit=1"

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url, headers={"User-Agent": "FastAPI-Example/1.0"})
        if resp.status_code != 200:
            return None

        data = resp.json()
        results = data.get("data", [])
        if not results:
            return None

        item = results[0]
        # Deezer returns different image fields for artists vs albums
        if entity_type == "artists":
            img_url = item.get("picture_medium") or item.get("picture_big")
        else:
            img_url = item.get("cover_medium") or item.get("cover_big")

        if not img_url:
            return None

        # Download the image
        dl = await client.get(img_url, follow_redirects=True)
        if dl.status_code != 200:
            return None

        ct = dl.headers.get("content-type", "image/jpeg")
        ext_map = {"image/jpeg": ".jpg", "image/png": ".png", "image/gif": ".gif", "image/webp": ".webp"}
        ext = ext_map.get(ct, ".jpg")

        # Remove old files
        for old_ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]:
            old = storage_dir / f"{entity_id}{old_ext}"
            if old.exists():
                old.unlink()

        dest = storage_dir / f"{entity_id}{ext}"
        dest.write_bytes(dl.content)
        return f"/static/images/{entity_type}/{entity_id}{ext}"


async def process(entity_type: str, model_cls, name_col: str, label: str):
    async with AsyncSessionLocal() as db:
        id_col = getattr(model_cls, "ArtistId" if entity_type == "artists" else "AlbumId")
        result = await db.execute(
            select(model_cls).where(model_cls.ImageUrl.is_(None)).order_by(id_col)
        )
        items = result.scalars().all()

    total = len(items)
    ok = 0
    failed = 0

    if not items:
        print(f"No remaining {label} to process.")
        return total, ok, failed

    print(f"Processing {total} {label} via Deezer...")
    for i, item in enumerate(items, 1):
        id_val = item.ArtistId if entity_type == "artists" else item.AlbumId
        name = getattr(item, name_col)
        if not name:
            failed += 1
            continue

        try:
            url = await fetch_image(entity_type, id_val, name)
            if url:
                async with AsyncSessionLocal() as db:
                    obj = await db.get(model_cls, id_val)
                    obj.ImageUrl = url
                    await db.commit()
                ok += 1
                print(f"  [{i}/{total}] OK   {name[:50]}")
            else:
                failed += 1
                print(f"  [{i}/{total}] FAIL {name[:50]}")
        except Exception as e:
            failed += 1
            print(f"  [{i}/{total}] FAIL {name[:50]}: {str(e)[:60]}")

        await asyncio.sleep(0.3)

    return total, ok, failed


async def main():
    start = time.time()
    art_t, art_ok, art_f = await process("artists", Artist, "Name", "artists")
    alb_t, alb_ok, alb_f = await process("albums", Album, "Title", "albums")
    elapsed = time.time() - start

    print(f"\n{'='*50}")
    print(f"Artists: {art_ok} OK / {art_f} FAIL (of {art_t})")
    print(f"Albums:  {alb_ok} OK / {alb_f} FAIL (of {alb_t})")
    print(f"Time: {elapsed:.1f}s")


if __name__ == "__main__":
    asyncio.run(main())
