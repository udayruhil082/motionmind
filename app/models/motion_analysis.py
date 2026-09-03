from sqlalchemy import Column, Numeric, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func

from app.db.database import Base


class MotionAnalysis(Base):
    __tablename__ = "motion_analyses"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False
    )

    session_id = Column(
        UUID(as_uuid=True),
        ForeignKey("practice_sessions.id"),
        nullable=False
    )

    overall_score = Column(
        Numeric,
        nullable=True
    )

    model_name = Column(
        String,
        nullable=False
    )

    model_version = Column(
        String,
        nullable=True
    )

    analysis_data = Column(
        JSONB,
        nullable=True
    )

    analyzed_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )