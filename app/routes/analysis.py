from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from uuid import UUID
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.motion_analysis import MotionAnalysis


router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"]
)


class AnalysisInput(BaseModel):
    session_id: UUID

    overall_score: float = Field(
        ge=0,
        le=100
    )

    model_name: str = "MotionMind-ML"

    model_version: str = "1.0"

    analysis_data: dict = {}


@router.post("/")
def save_analysis(
    data: AnalysisInput,
    db: Session = Depends(get_db)
):
    try:
        analysis = MotionAnalysis(
            session_id=data.session_id,
            overall_score=data.overall_score,
            model_name=data.model_name,
            model_version=data.model_version,
            analysis_data=data.analysis_data
        )

        db.add(analysis)
        db.commit()
        db.refresh(analysis)

        return {
            "message": "Motion analysis saved successfully",
            "analysis_id": str(analysis.id),
            "session_id": str(analysis.session_id),
            "overall_score": analysis.overall_score,
            "model_name": analysis.model_name,
            "model_version": analysis.model_version,
            "analysis_data": analysis.analysis_data,
            "analyzed_at": analysis.analyzed_at
        }

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get("/{session_id}")
def get_analysis(
    session_id: UUID,
    db: Session = Depends(get_db)
):
    analysis = (
        db.query(MotionAnalysis)
        .filter(MotionAnalysis.session_id == session_id)
        .order_by(MotionAnalysis.created_at.desc())
        .first()
    )

    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="No analysis found for this session"
        )

    return {
        "analysis_id": str(analysis.id),
        "session_id": str(analysis.session_id),
        "overall_score": analysis.overall_score,
        "model_name": analysis.model_name,
        "model_version": analysis.model_version,
        "analysis_data": analysis.analysis_data,
        "analyzed_at": analysis.analyzed_at
    }