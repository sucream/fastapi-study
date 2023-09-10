from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    SQLAlchemy 2.0 이후로는 DeclarativeBase를 상속받아야 함
    본 클래스는 모든 모델의 베이스 클래스
    """
    pass