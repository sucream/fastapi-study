from fastapi_study.models import Base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# 메모리로만 사용
DB_URL = "sqlite:///:memory:"

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    DB 세션을 생성합니다.
    """
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

def create_all_tables():
    """
    Base 클래스를 상속한 모든 모델의 테이블을 생성합니다.
    """
    
    Base.metadata.create_all(bind=engine)