from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from app.auth import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.db.database import get_db
from app.models.profile import Profile


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# ---------------------------------
# REQUEST MODELS
# ---------------------------------

class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str
    age: int | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ---------------------------------
# SIGNUP
# ---------------------------------

@router.post("/signup")
def signup(
    data: SignupRequest,
    db: Session = Depends(get_db)
):
    existing_user = (
        db.query(Profile)
        .filter(Profile.email.ilike(data.email))
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists"
        )

    user = Profile(
        id=uuid4(),
        full_name=data.full_name,
        age=data.age,
        email=data.email.lower(),
        password_hash=hash_password(data.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    access_token = create_access_token(user.id)

    return {
        "message": "Account created successfully",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(user.id),
            "email": user.email,
            "full_name": user.full_name,
            "age": user.age
        }
    }


# ---------------------------------
# LOGIN
# ---------------------------------

@router.post("/login")
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):
    user = (
        db.query(Profile)
        .filter(Profile.email.ilike(data.email))
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not user.password_hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This account needs to be registered again"
        )

    if not verify_password(
        data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(user.id)

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(user.id),
            "email": user.email,
            "full_name": user.full_name,
            "age": user.age
        }
    }


# ---------------------------------
# CURRENT USER
# ---------------------------------

@router.get("/me")
def get_me(
    current_user: Profile = Depends(
        __import__("app.auth", fromlist=["get_current_user"]).get_current_user
    )
):
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "full_name": current_user.full_name,
        "age": current_user.age
    }