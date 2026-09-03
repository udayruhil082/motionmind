from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from uuid import UUID
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.practice_session import PracticeSession


router = APIRouter(
    prefix="/sessions",
    tags=["Sessions"]
)


class SessionCreate(BaseModel):
    user_id: UUID
    skill_id: UUID
    duration_seconds: int


@router.post("/")
def create_session(
    data: SessionCreate,
    db: Session = Depends(get_db)
):
    try:
        new_session = PracticeSession(
            user_id=data.user_id,
            skill_id=data.skill_id,
            duration_seconds=data.duration_seconds,
            status="completed"
        )

        db.add(new_session)
        db.commit()
        db.refresh(new_session)

        return {
            "message": "Practice session created successfully",
            "session_id": str(new_session.id),
            "user_id": str(new_session.user_id),
            "skill_id": str(new_session.skill_id),
            "duration_seconds": new_session.duration_seconds,
            "status": new_session.status,
            "created_at": new_session.created_at
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get("/")
def get_sessions(
    db: Session = Depends(get_db)
):
    sessions = (
        db.query(PracticeSession)
        .order_by(PracticeSession.created_at.desc())
        .all()
    )

    return {
        "count": len(sessions),
        "sessions": [
            {
                "id": str(session.id),
                "user_id": str(session.user_id),
                "skill_id": str(session.skill_id),
                "duration_seconds": session.duration_seconds,
                "status": session.status,
                "created_at": session.created_at
            }
            for session in sessions
        ]
    }