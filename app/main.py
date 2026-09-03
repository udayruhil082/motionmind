from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.auth import router as auth_router
from app.routes.session import router as session_router
from app.routes.analysis import router as analysis_router
from app.routes.dashboard import router as dashboard_router


app = FastAPI(
    title="MotionMind API",
    description="Backend API for MotionMind AI Motion Analysis",
    version="1.0.0"
)


# Allow our React frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# API routes
app.include_router(auth_router)
app.include_router(session_router)
app.include_router(analysis_router)
app.include_router(dashboard_router)


# Health check
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "MotionMind Backend"
    }