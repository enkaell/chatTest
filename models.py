from sqlalchemy import Column, Integer, String, LargeBinary, Table, ForeignKey
from db_init import Base
from sqlalchemy.orm import relationship


class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True, index=True)
    chat_name = Column(String)


association_table = Table(
    "association_table",
    Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("chat_id", ForeignKey("chats.id")),
)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    userinfo = Column(String)
    username = Column(String, unique=True, index=True)
    avatar_50 = Column(LargeBinary)
    avatar_100 = Column(LargeBinary)
    avatar_400 = Column(LargeBinary)
    phone = Column(String, unique=True, index=True)
    password_hash = Column(String)
    token = Column(String)
    chat = relationship("Chat", secondary=association_table, backref="parents")
