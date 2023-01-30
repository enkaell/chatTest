from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException, status
import requests
from models import User
from jose import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def validate_password(plain_password, hashed_password):
    if not pwd_context.verify(plain_password, hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")


def get_password_hash(password):
    return pwd_context.hash(password)


def validate_register_data(user, db: Session):
    if db.query(User).filter(or_(User.username == user.username, User.phone == user.phone)).all():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    # regex phone validation
    db.add(User(username=user.username, password_hash=get_password_hash(user.password), phone=user.phone))
    db.commit()


def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=1400)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, "PrettyFlowSecretKey", algorithm="HS256")
    return encoded_jwt


def login_user(form_data: dict, db: Session):
    if user := db.query(User).filter(User.phone == form_data.username).one_or_none():
        validate_password(form_data.password, user.password_hash)
        user.token = create_token(data={'sub': user.phone})
        db.add(user)
        db.commit()
        return user.token
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
