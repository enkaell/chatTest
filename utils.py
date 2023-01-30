import base64
from PIL import Image
from users.schemas import UserRegisterSchema, UserLoginSchema, UserEditSchema
from models import User, Chat, association_table
import logging
from tempfile import SpooledTemporaryFile
from fastapi import HTTPException, status
from auth.utils import get_password_hash
from db_init import get_session


def edit_user_profile(file: SpooledTemporaryFile, user: UserEditSchema, db, user_id):
    if db.query(User).filter_by(username=user.username).first() and user.username is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    if file:
        avatars = crop_avatar_file(file)
        db.query(User).filter_by(id=user_id).update({"avatar_50": avatars[0], "avatar_100": avatars[1],
                                                     "avatar_400": avatars[2]})
    if user.password_hash:
        user.password_hash = get_password_hash(user.password_hash)
    if user := {k: v for k, v in dict(user).items() if v is not None}:
        db.query(User).filter_by(id=user_id).update(user)
    db.commit()
    user['password_hash'] = "*" * len(user['password_hash'])
    return user


def crop_avatar_file(file: SpooledTemporaryFile):
    sizes = [50, 100, 400]
    avatars = []
    image = Image.open(file, mode="r")
    try:
        for size in sizes:
            avatars.append(base64.b64encode(image.crop((0, 0, size, size)).tobytes()))
    except Exception as e:
        logging.error(f"PIL exception: {e}")
    return avatars


def create_chat_by_user(chat, db, user_id):
    user = db.query(User).filter_by(id=user_id).first()
    chat_row = Chat(chat_name=chat.chat_name)
    user.chat.append(chat_row)
    db.commit()
    return {"message": "Chat created"}


def get_all_chats(db, user_id):
    chats = []
    for chat in db.query(association_table).filter_by(user_id=user_id):
        chats.append(db.query(Chat).filter_by(id=chat[1]).first().chat_name)
    return chats


def delete_user_chat(chat_id, db, user_id):
    user = db.query(User).filter_by(id=user_id).first()
    chat = db.query(Chat).filter_by(id=chat_id).first()
    if chat in user.chat:
        user.chat.remove(chat)
        db.delete(chat)
    db.commit()
    return {"message": "Chat is deleted"}


def check_valid_token(bearer: str):
    db = next(get_session())
    return db.query(User).filter_by(token=bearer).one_or_none()


def get_chat_name_by_id(chat_id: int):
    db = next(get_session())
    if chat := db.query(Chat).filter_by(id=chat_id).one_or_none():
        return chat.chat_name
