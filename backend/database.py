import导入 os导入 os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_DIR = "/opt/render/project/src/backend"

try:尝试:
    os.makedirs创建目录(DATABASE_DIR, exist_ok=True)数据库目录，exist_ok=True)数据库目录，exist_ok=True)
except except except except except except except except except except except except except except except Exception:异常:异常:异常:异常：异常：异常：异常：异常：异常：异常：异常：异常：异常：异常：异常：异常：异常：异常：异常：异常：异常：异常：异常：异常：异常：
    DATABASE_DIR = "/tmp"

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_DIR}/finance.db"

engine = create_engine(引擎 =create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()基类 =declarative_base()基类 =declarative_base声明式基类声明式基类()基类 =declarative_base声明式基类声明式基类()

def get_db():
    db = SessionLocal()
    try:尝试:尝试:尝试:
        yield db
    finally:
        db.close()db.关闭()数据库。关闭()
