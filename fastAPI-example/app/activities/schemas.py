from datetime import datetime
from typing import Optional

from app.core.schemas import CustomModel


class ActivityResponse(CustomModel):
    activity_id: int
    timestamp: datetime
    username: str
    action_type: str
    detail: Optional[str] = None
