from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

POSTGRESQL_DATABASE_URL = "postgresql://admin:admin@db/chat"

engine = create_engine(
    POSTGRESQL_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def connect_db():
    try:
        engine.connect()
    except Exception as e:
        print(f"Database conn error: {e}")
    print(f"Connection {engine.url}")


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.commit()
        session.close()
