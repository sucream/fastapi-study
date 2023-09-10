from . import Base  # __init__.py에서 Base 클래스를 가져옴

from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import mapped_column, Mapped


class ToDo(Base):
    """
    ToDo 모델
    
    Parameters
    ----------
    id : int
        고유 id
    contents : str
        할 일 내용
    is_done : bool
        완료 여부

    """
    
    __tablename__ = "todo"
    
    # Mapped[int]는 타입 힌트를 위한 것
    # mapped_column은 SQLAlchemy에서 명시적으로 orm을 사용하는 컬럼을 위한 것
    id: Mapped[int] = mapped_column(primary_key=True)
    contents: Mapped[str] = mapped_column(String(256), nullable=False)
    is_done: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)