from fastapi_study.models import Base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# 메모리로만 사용
MEMORY_DB_URL = "sqlite:///:memory:"
# MARIADB_URL = "mysql+pymysql://root:root@localhost:3306/todo?charset=utf8mb4"

engine = create_engine(MEMORY_DB_URL, connect_args={"check_same_thread": False})
# engine = create_engine(MARIADB_URL)
test_engine = create_engine(MEMORY_DB_URL, connect_args={"check_same_thread": False})
# test_engine = create_engine(MARIADB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

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