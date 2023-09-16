import datetime

from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column


class Base(DeclarativeBase):
    """
    SQLAlchemy 2.0 이후로는 DeclarativeBase를 상속받아야 함
    본 클래스는 모든 모델의 베이스 클래스
    """

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
