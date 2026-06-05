"""
Batch script: fetch reference images for all artists and albums from Wikipedia.

Usage:
    python scripts/fetch_all_images.py
"""

import asyncio
import sys
import time
from pathlib import Path

# Ensure project root is in path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.database import AsyncSessionLocal
from app.core.image_service import fetch_from_wikipedia
from app.artists.model import Artist
from app.albums.model import Album
from sqlalchemy import select


async def process_artists():
    """Fetch images for all artists that don't already have one."""
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Artist).order_by(Artist.ArtistId))
        artists = result.scalars().all()

    total = len(artists)
    ok = 0
    skipped = 0
    failed = 0

    print(f"Processing {total} artists...")
    for i, artist in enumerate(artists, 1):
        if artist.ImageUrl:
            skipped += 1
            print(f"  [{i}/{total}] SKIP {artist.Name} (already has image)")
            continue

        try:
            url = await fetch_from_wikipedia("artists", artist.ArtistId, artist.Name)
            # Update in DB
            async with AsyncSessionLocal() as db:
                a = await db.get(Artist, artist.ArtistId)
                a.ImageUrl = url
                await db.commit()
            ok += 1
            print(f"  [{i}/{total}] OK   {artist.Name} -> {url.split('/')[-1]}")
        except Exception as e:
            failed += 1
            print(f"  [{i}/{total}] FAIL {artist.Name}: {e}")

        await asyncio.sleep(1)  # Rate limit

    return total, ok, skipped, failed


async def process_albums():
    """Fetch cover images for all albums that don't already have one."""
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Album).order_by(Album.AlbumId))
        albums = result.scalars().all()

    total = len(albums)
    ok = 0
    skipped = 0
    failed = 0

    print(f"\nProcessing {total} albums...")
    for i, album in enumerate(albums, 1):
        if album.ImageUrl:
            skipped += 1
            print(f"  [{i}/{total}] SKIP {album.Title} (already has image)")
            continue

        try:
            url = await fetch_from_wikipedia("albums", album.AlbumId, album.Title)
            async with AsyncSessionLocal() as db:
                a = await db.get(Album, album.AlbumId)
                a.ImageUrl = url
                await db.commit()
            ok += 1
            print(f"  [{i}/{total}] OK   {album.Title} -> {url.split('/')[-1]}")
        except Exception as e:
            failed += 1
            print(f"  [{i}/{total}] FAIL {album.Title}: {e}")

        await asyncio.sleep(1)

    return total, ok, skipped, failed


async def main():
    start = time.time()

    art_total, art_ok, art_skip, art_fail = await process_artists()
    alb_total, alb_ok, alb_skip, alb_fail = await process_albums()

    elapsed = time.time() - start
    print(f"\n{'='*50}")
    print(f"Artists: {art_ok} OK / {art_skip} skipped / {art_fail} failed (of {art_total})")
    print(f"Albums:  {alb_ok} OK / {alb_skip} skipped / {alb_fail} failed (of {alb_total})")
    print(f"Total time: {elapsed:.1f}s")


if __name__ == "__main__":
    asyncio.run(main())
