from sqlalchemy import Boolean, Column, Integer, String

from app.core.database import Base


class User(Base):
    __tablename__ = "User"

    user_id = Column("UserId", Integer, primary_key=True)
    username = Column("Username", String(80), unique=True, index=True, nullable=False)
    email = Column("Email", String(120), unique=True, index=True, nullable=False)
    full_name = Column("FullName", String(120), nullable=True)
    disabled = Column("Disabled", Boolean, default=False, nullable=False)
    is_admin = Column("IsAdmin", Boolean, default=False, nullable=False)
    hashed_password = Column("HashedPassword", String(255), nullable=False)
