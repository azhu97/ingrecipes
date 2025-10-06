import bcrypt
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import models

def create_user(db: Session, name: str, email: str, hashed_password: str) -> models.User:
    new_user = models.User(
        name = name,
        email = email, 
        hashed_password = hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_email(db: Session, email: str) -> models.User:
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_user_by_id(db: Session, user_id: int) -> models.User:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_all_users(db: Session) -> list[models.User]:
    return db.query(models.User).all()

def delete_user(db: Session, user_id: int) -> bool:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return True

def hash_password(plain_password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def update_user_password(db: Session, user_id: int, new_password: str) -> models.User:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.hashed_password = hash_password(new_password)

    db.commit()
    db.refresh(user)
    return user

def delete_all_users(db: Session) -> None:
    db.query(models.User).delete()
    db.commit()