from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.dependencies import dep_from_app_state, StateAttrs
from app.models.users import UserCreate
from app.db.models.users import User
from app.dependencies import get_current_user

from app.db import database
from app.services import ServiceLayer


router = APIRouter()

@router.post("/register")
async def register_user(user: UserCreate, db: Session = Depends(database.get_db), service: ServiceLayer = dep_from_app_state(StateAttrs.services)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = service.password_service.hash_password(user.password_)
    new_user = User(**user.dict(exclude={'password_'}), hashed_password=hashed_password, created_at=datetime.now())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db), service: ServiceLayer = dep_from_app_state(StateAttrs.services)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not service.password_service.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = service.password_service.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/secure")
async def endpoint(current_user: User = Depends(get_current_user)):
    return {"msg": "you are in", "user": current_user.username}
