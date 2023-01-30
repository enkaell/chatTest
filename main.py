import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Request, File, UploadFile
from db_init import connect_db, get_session
from users.schemas import UserRegisterSchema, UserLoginSchema, UserEditSchema, Chat
from users.utils import get_user_id_by_phone
from sqlalchemy.orm import Session
from auth.utils import login_user, validate_register_data
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from fastapi.openapi.utils import get_openapi
from utils import edit_user_profile, create_chat_by_user, get_all_chats, delete_user_chat

tags_metadata = [
    {
        "name": "profile",
        "description": "Profile requests",
    },
    {
        "name": "chats",
        "description": "Chat requests",
    },
]

app = FastAPI()
connect_db()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/token')


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Test Chat App",
        version="v1.0.0",
        description="A custom chat app based on SocketIO",
        routes=app.routes,
        tags=tags_metadata,
        contact={"Github": "@enkaell", "Telegram": "@nkl249"}
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)):
    try:
        payload = jwt.decode(token, "PrettyFlowSecretKey", algorithms="HS256")
        phone: str = payload.get("sub")
        if phone is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")
    if user_id := get_user_id_by_phone(phone, db):
        return user_id
    else:
        HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")


@app.post("/register", tags=['profile'])
def register(user: UserRegisterSchema = Depends(), db: Session = Depends(get_session)):
    validate_register_data(user, db)
    return {"message": "Register successfully"}


@app.post("/token", tags=['profile'])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    token = login_user(form_data, db)
    return {'access_token': token, 'token_type': 'bearer'}


@app.put("/edit", tags=['profile'])
def edit_profile(file: UploadFile = None, user: UserEditSchema = Depends(), db: Session = Depends(get_session),
                 user_id: int = Depends(get_current_user)):
    return edit_user_profile(file.file if file else None, user, db, user_id)


@app.post("/chat/create", tags=['chats'])
def create_chat(chat: Chat = Depends(), db: Session = Depends(get_session), user_id: int = Depends(get_current_user)):
    return create_chat_by_user(chat, db, user_id)


@app.get("/chats", tags=['chats'])
def get_chats(db: Session = Depends(get_session), user_id: int = Depends(get_current_user)):
    return get_all_chats(db, user_id)


@app.delete("/chats/{chat_id}", tags=['chats'])
def delete_chat(chat_id: int, db: Session = Depends(get_session), user_id: int = Depends(get_current_user)):
    return delete_user_chat(chat_id, db, user_id)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7777)
