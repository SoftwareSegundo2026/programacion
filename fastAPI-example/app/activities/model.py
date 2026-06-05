from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from app.core.database import Base


class Activity(Base):
    __tablename__ = "Activity"

    activity_id = Column("ActivityId", Integer, primary_key=True)
    timestamp = Column("Timestamp", DateTime, default=datetime.utcnow, nullable=False)
    username = Column("Username", String(80), nullable=False)
    action_type = Column("ActionType", String(20), nullable=False)
    detail = Column("Detail", String(500), nullable=True)
