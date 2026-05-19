from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.core.security import get_password_hash

from .model import User

logger = get_logger(__name__)


DEMO_USERS = [
    {
        "username": "admin",
        "email": "admin@example.com",
        "full_name": "Demo Admin",
        "disabled": False,
        "password": "admin123",
    },
    {
        "username": "reader",
        "email": "reader@example.com",
        "full_name": "Demo Reader",
        "disabled": True,
        "password": "reader123",
    },
]


async def seed_demo_users(db: AsyncSession) -> None:
    """Insert the demo users used by the authentication example."""
    result = await db.execute(select(User.username))
    existing_usernames = set(result.scalars().all())

    created_users = []
    for demo_user in DEMO_USERS:
        if demo_user["username"] in existing_usernames:
            continue

        created_users.append(
            User(
                username=demo_user["username"],
                email=demo_user["email"],
                full_name=demo_user["full_name"],
                disabled=demo_user["disabled"],
                hashed_password=get_password_hash(demo_user["password"]),
            )
        )

    if not created_users:
        logger.debug("seed_demo_users - no demo users to seed")
        return

    db.add_all(created_users)
    await db.commit()
    logger.info("seed_demo_users - seeded %s demo users", len(created_users))