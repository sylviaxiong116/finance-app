import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_DIR = "/opt/render/project/src/backend"

try:
    os.makedirs(DATABASE_DIR, exist_ok=True)
except Exception:
    DATABASE_DIR = "/tmp"

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_DIR}/finance.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
