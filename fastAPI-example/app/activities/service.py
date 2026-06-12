from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.model import User as UserModel
from app.core.logging import get_logger

from .model import Activity as ActivityModel
from .schemas import ActivityResponse

logger = get_logger(__name__)


async def _get_admin_usernames(db: AsyncSession) -> list[str]:
    result = await db.execute(select(UserModel.username).where(UserModel.is_admin))
    return [row[0] for row in result.fetchall()]


async def log_activity(
    db: AsyncSession,
    username: str,
    action_type: str,
    detail: str | None = None,
) -> None:
    """Crea un registro de auditoría (ej: 'admin creó artista X'). Se usa en cada operación importante."""
    entry = ActivityModel(
        timestamp=datetime.utcnow(),
        username=username,
        action_type=action_type,
        detail=detail,
    )
    db.add(entry)
    logger.info("Activity logged: %s - %s - %s", action_type, username, detail)


async def list_activities(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    caller_is_admin: bool = False,
) -> list[ActivityResponse]:
    """Lista las actividades. Los usuarios no admin NO ven las actividades de usuarios admin."""
    query = select(ActivityModel).order_by(ActivityModel.activity_id.desc())
    if not caller_is_admin:
        admin_usernames = await _get_admin_usernames(db)
        if admin_usernames:
            query = query.where(ActivityModel.username.notin_(admin_usernames))
    result = await db.execute(query.offset(skip).limit(limit))
    return [ActivityResponse.model_validate(row) for row in result.scalars().all()]
