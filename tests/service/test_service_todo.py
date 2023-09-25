from unittest.mock import Mock, ANY

from fastapi_study.models.todo import ToDo as TodoModel
from fastapi_study.schemas.todo import ToDoRead, ToDoCreate, ToDoUpdate
from fastapi_study.services.todo import ToDoService

import pytest
from pytest_mock.plugin import MockerFixture
from sqlalchemy.orm import Session


def test_create_new_todo(mocker: MockerFixture, mock_todo_servicc: ToDoService):
    # 서비스 함수 호출
    input_todo = ToDoCreate(contents="Test", is_done=False)
    expected_todo = ToDoRead(
        id=1,
        contents="Test",
        is_done=False,
        created_at="2021-10-01T00:00:00+09:00",
        updated_at="2021-10-01T00:00:00+09:00"
    )
    
    created_todo = mock_todo_servicc.create_new_todo(input_todo)

    # 반환값, DB 세션의 호출 등을 검증
    assert created_todo.id == expected_todo.id
    assert expected_todo.contents == created_todo.contents
    assert created_todo.is_done == expected_todo.is_done
    

@pytest.fixture
def insert_test_data(mock_db_session: Session):
    """
    테스트를 위한 데이터를 DB에 삽입하는 fixture
    """
    input_todo = ToDoCreate(contents="Test", is_done=False)
    input_todo = TodoModel(**input_todo.model_dump())
    mock_db_session.add(input_todo)
    mock_db_session.commit()
    mock_db_session.refresh(input_todo)
    yield
    mock_db_session.delete(input_todo)
    mock_db_session.commit()
    

def test_update_todo_success(mocker: MockerFixture, mock_todo_servicc: ToDoService, insert_test_data):
    # 서비스 함수 호출
    input_todo = ToDoUpdate(contents="Test", is_done=True)
    expected_todo = ToDoRead(
        id=1,
        contents="Test",
        is_done=True,
        created_at="2021-10-01T00:00:00+09:00",
        updated_at="2021-10-01T00:00:00+09:00"
    )
    
    updated_todo = mock_todo_servicc.update_todo(1, input_todo)

    # 반환값, DB 세션의 호출 등을 검증
    assert expected_todo.id == updated_todo.id
    assert expected_todo.contents == updated_todo.contents
    assert expected_todo.is_done == updated_todo.is_done