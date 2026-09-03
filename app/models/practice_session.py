from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.database import Base


class PracticeSession(Base):
    __tablename__ = "practice_sessions"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("profiles.id"),
        nullable=False
    )

    skill_id = Column(
        UUID(as_uuid=True),
        ForeignKey("skills.id"),
        nullable=False
    )

    started_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    ended_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    duration_seconds = Column(
        Integer,
        nullable=True
    )

    model_name = Column(
        String,
        nullable=True
    )

    status = Column(
        String,
        nullable=False,
        default="started"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )