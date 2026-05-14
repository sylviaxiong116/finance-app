import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Render 上可写的目录：/opt/render/project/src/backend
# 使用当前脚本所在目录作为数据库路径
_current_dir = os.path.dirname(os.path.abspath(__file__))
# 尝试使用当前目录，如果失败则使用 /tmp
DATABASE_DIR = os.environ.get("DATABASE_DIR", _current_dir)

# 确保目录存在且可写
try:
    os.makedirs(DATABASE_DIR, exist_ok=True)
except Exception:
    # 如果失败，尝试使用 /tmp 目录
    DATABASE_DIR = "/tmp"
    try:
        os.makedirs(DATABASE_DIR, exist_ok=True)
    except Exception:
        DATABASE_DIR = _current_dir

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
