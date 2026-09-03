from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.database import get_db
from app.models.practice_session import PracticeSession
from app.models.motion_analysis import MotionAnalysis


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/")
def get_dashboard(
    db: Session = Depends(get_db)
):
    # Total practice sessions
    total_sessions = (
        db.query(func.count(PracticeSession.id))
        .scalar()
        or 0
    )

    # Average score
    average_score = (
        db.query(func.avg(MotionAnalysis.overall_score))
        .scalar()
    )

    # Best score
    best_score = (
        db.query(func.max(MotionAnalysis.overall_score))
        .scalar()
    )

    # Number of analysed sessions
    analysed_sessions = (
        db.query(func.count(MotionAnalysis.id))
        .scalar()
        or 0
    )

    # Recent sessions
    recent_sessions = (
        db.query(
            PracticeSession,
            MotionAnalysis
        )
        .outerjoin(
            MotionAnalysis,
            PracticeSession.id == MotionAnalysis.session_id
        )
        .order_by(
            PracticeSession.created_at.desc()
        )
        .limit(10)
        .all()
    )

    recent = []

    for session, analysis in recent_sessions:
        recent.append({
            "session_id": str(session.id),
            "skill_id": str(session.skill_id),
            "duration_seconds": session.duration_seconds,
            "status": session.status,
            "score": (
                analysis.overall_score
                if analysis
                else None
            ),
            "created_at": session.created_at
        })

    return {
        "total_sessions": total_sessions,
        "analysed_sessions": analysed_sessions,
        "average_score": (
            round(float(average_score), 2)
            if average_score is not None
            else 0
        ),
        "best_score": (
            float(best_score)
            if best_score is not None
            else 0
        ),
        "recent_sessions": recent
    }