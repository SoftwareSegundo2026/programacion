"""
Continue fetching remaining artists and album images (skip those already done).
"""
import asyncio, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.database import AsyncSessionLocal
from app.artists.model import Artist
from app.albums.model import Album
from sqlalchemy import select, text
import httpx


async def fetch_one(entity_type: str, entity_id: int, query: str) -> str | None:
    """Simplified fetch: search Wikipedia, download image, save to disk."""
    storage_dir = Path("./static/images") / entity_type
    storage_dir.mkdir(parents=True, exist_ok=True)

    headers = {"User-Agent": "FastAPI-Example/1.0 (course project)"}
    search_url = "https://en.wikipedia.org/w/api.php"

    async with httpx.AsyncClient(timeout=10) as client:
        sp = {"action": "query", "list": "search", "srsearch": query, "format": "json", "srlimit": 1}
        sr = await client.get(search_url, params=sp, headers=headers)
        if sr.status_code != 200:
            return None
        data = sr.json()
        results = data.get("query", {}).get("search", [])
        if not results:
            return None

        title = results[0]["title"]
        ip = {"action": "query", "titles": title, "prop": "pageimages", "format": "json", "pithumbsize": 300}
        ir = await client.get(search_url, params=ip, headers=headers)
        if ir.status_code != 200:
            return None
        img_data = ir.json()
        pages = img_data.get("query", {}).get("pages", {})
        thumb = None
        for p in pages.values():
            thumb = p.get("thumbnail")
            break
        if not thumb or "source" not in thumb:
            return None

        dl_headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://en.wikipedia.org/"}
        dr = await client.get(thumb["source"], headers=dl_headers, follow_redirects=True)
        if dr.status_code != 200:
            return None

        ct = dr.headers.get("content-type", "image/jpeg")
        ext = {"image/jpeg": ".jpg", "image/png": ".png", "image/gif": ".gif", "image/webp": ".webp"}
        ext_suffix = ext.get(ct, ".jpg")

        # Remove old files for this ID
        for old_ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]:
            old = storage_dir / f"{entity_id}{old_ext}"
            if old.exists():
                old.unlink()

        dest = storage_dir / f"{entity_id}{ext_suffix}"
        dest.write_bytes(dr.content)
        return f"/static/images/{entity_type}/{entity_id}{ext_suffix}"


async def process(entity_type: str, model_cls, name_col: str):
    """Process all entities of a type that lack ImageUrl."""
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(model_cls).where(model_cls.ImageUrl.is_(None)).order_by(model_cls.ArtistId if entity_type == "artists" else model_cls.AlbumId)
        )
        items = result.scalars().all()

    total = len(items)
    ok = 0
    failed = 0

    if not items:
        print(f"No remaining {entity_type} to process.")
        return total, ok, failed

    print(f"Processing {total} {entity_type}...")
    for i, item in enumerate(items, 1):
        id_col = item.ArtistId if entity_type == "artists" else item.AlbumId
        name = getattr(item, name_col)
        name_clean = name if name else str(id_col)

        try:
            url = await fetch_one(entity_type, id_col, name_clean)
            if url:
                async with AsyncSessionLocal() as db:
                    obj = await db.get(model_cls, id_col)
                    obj.ImageUrl = url
                    await db.commit()
                ok += 1
                print(f"  [{i}/{total}] OK   {name_clean[:50]}")
            else:
                failed += 1
                print(f"  [{i}/{total}] FAIL {name_clean[:50]} (no image found)")
        except Exception as e:
            failed += 1
            print(f"  [{i}/{total}] FAIL {name_clean[:50]}: {str(e)[:60]}")

        await asyncio.sleep(0.3)

    return total, ok, failed


async def main():
    start = time.time()

    art_total, art_ok, art_fail = await process("artists", Artist, "Name")
    alb_total, alb_ok, alb_fail = await process("albums", Album, "Title")

    elapsed = time.time() - start
    print(f"\n{'='*50}")
    print(f"Artists: {art_ok} OK / {art_fail} failed (of {art_total})")
    print(f"Albums:  {alb_ok} OK / {alb_fail} failed (of {alb_total})")
    print(f"Time: {elapsed:.1f}s")


if __name__ == "__main__":
    asyncio.run(main())
