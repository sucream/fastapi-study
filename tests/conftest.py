import logging
from unittest.mock import Mock

from main import app
from fastapi_study.services.todo import ToDoService

import pytest
from pytest_mock.plugin import MockerFixture
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def mock_init_db():
    """
    테스트를 위한 DB 초기화
    """
    logging.info("<<INIT DB>>")
    from fastapi_study.database import Base, test_engine, TestSessionLocal
    Base.metadata.create_all(bind=test_engine)
    sees = TestSessionLocal()
    yield sees
    sees.close()
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture
def mock_db_session(mocker: MockerFixture, mock_init_db) -> Session:
    """
    테스트를 위한 DB 세션
    """
    
    logging.info("<<INIT DB SESSION>>")
    session = mock_init_db
    session.begin()  # 트랜잭션 시작
    yield session
    session.rollback()  # 롤백
    session.close()

    
@pytest.fixture
def mock_todo_servicc(mocker: MockerFixture, mock_db_session: Session) -> ToDoService:
    """
    todo_service를 테스트하기 위한 fixture
    """
    
    return ToDoService(db=mock_db_session)