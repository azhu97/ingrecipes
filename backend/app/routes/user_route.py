from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
import app.services.user_service as user_service

router = APIRouter(
    prefix = "/users",
    tags = ["users"]
)

# user signup
@router.post("/signup")
def signup_user(name: str, password: str, email: str, db: Session = Depends(get_db)) -> dict:
    hashed_password = user_service.hash_password(password)
    user = user_service.create_user(db=db, name=name, email=email, hashed_password=hashed_password)
    if not user:
        raise HTTPException(status_code=400, detail="User already exists")
    return {"message": "User successfully created", "user_id": user.id} 

# get user by email
@router.get("/email/{email}")
def get_user_by_email(email: str, db: Session = Depends(get_db)) -> user_service.models.User:
    user = user_service.get_user_by_email(db=db, email=email)
    return user

# get user by id 
@router.get("/{user_id}")
def get_user_by_id(user_id: int, db: Session = Depends(get_db)) -> user_service.models.User:
    user = user_service.get_user_by_id(db=db, user_id=user_id)
    return user

# get all users
@router.get("/")
def get_all_users(db: Session = Depends(get_db)) -> list[user_service.models.User]:
    users = user_service.get_all_users(db=db)
    return users



