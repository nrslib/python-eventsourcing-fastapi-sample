from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# データベースの URL
DATABASE_URL = 'sqlite:///./db/sqlite.db'

# エンジンの作成
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# セッションローカルの設定
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ベースクラスの作成
Base = declarative_base()


# テーブルの作成
def init_db():
    Base.metadata.create_all(bind=engine)
