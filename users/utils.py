from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException, status
import requests
from models import User
from jose import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext


def get_user_id_by_phone(phone: str, db: Session):
    return db.query(User).filter_by(phone=phone).one_or_none().id

