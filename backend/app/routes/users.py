# backend/app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import get_db
from app.oauth2 import get_current_user
from app.models import User
from app.routes.auth import require_role

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# Get all users (only admins)
@router.get("/", response_model=list[schemas.UserResponse])
def read_users(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(require_role("admin"))  # ✅ only admins allowed
):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

# Get current logged-in user
@router.get("/me", response_model=schemas.UserResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user
# Get user by ID
@router.get("/{user_id}", response_model=schemas.UserResponse)
def read_user(
    user_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # ✅ allow only admin or the user themselves
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this user")

    return db_user


# Create new user
@router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

