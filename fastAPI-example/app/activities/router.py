from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_optional_user
from app.users.schemas import UserInDB
from app.core.database import get_db

from .schemas import ActivityResponse
from .service import list_activities

router = APIRouter(prefix="/activities", tags=["activities"])


@router.get("", response_model=list[ActivityResponse])
async def read_activities(
    db: AsyncSession = Depends(get_db),
    current_user: UserInDB | None = Depends(get_optional_user),
    skip: int = 0,
    limit: int = 100,
) -> list[ActivityResponse]:
    """GET /activities - Devuelve actividades paginadas. Si el usuario no es admin, oculta actividades de admins."""
    caller_is_admin = current_user is not None and current_user.is_admin and not current_user.disabled
    return await list_activities(db, skip, limit, caller_is_admin)
