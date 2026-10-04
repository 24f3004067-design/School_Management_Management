from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from config.auth import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password
)

from config.db import get_db
from models.user import User, UserRole
from schemas.auth import (TokenResponse,UserRegister,UserResponse,UserLogin)


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


# Register
@router.post("/register",response_model=UserResponse, status_code=201)
def register(data: UserRegister,db: Session = Depends(get_db)):
    
    user = User(
        username=data.username,
        email=data.email,
        hashed_password=hash_password(data.password),
        role=data.role,
        is_active=True,
    )

    db.add(user)

    try:
        db.commit()
        db.refresh(user)

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Username or email already exists"
        )

    return user


# Login
@router.post(
    "/login",
    response_model=TokenResponse
)
def login(data: UserLogin,db: Session = Depends(get_db)):
    user = (
        db.query(User)
        .filter(User.username == data.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password(
        data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="User is inactive"
        )

    token = create_access_token(str(user.id))

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# Get current user
def get_current_user(
    authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    try:
        # "Bearer token"
        token = authorization.replace("Bearer ", "")
        user_id = int(decode_access_token(token))

    except (ValueError, TypeError):
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    user = db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="User is inactive"
        )

    return user


# My profile
@router.get("/me",response_model=UserResponse)
def current_user(user: User = Depends(get_current_user)):
    return user


# Role checking
def require_roles(*roles: UserRole):
    def check_role(user: User = Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(
                status_code=403,
                detail="You don't have permission"
            )
        return user
    return check_role



