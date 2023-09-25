from unittest.mock import ANY

from fastapi_study.schemas.todo import ToDoRead, ToDoCreate, ToDoUpdate
from fastapi_study.services.todo import ToDoService

from pytest_mock.plugin import MockerFixture
from fastapi.testclient import TestClient

def test_get_all_todos(client: TestClient, mocker: MockerFixture):
    mock_return_value: list[ToDoRead] = [
        ToDoRead(id=1, contents="할 일 내용", is_done=False, created_at="2021-10-01T00:00:00+09:00", updated_at="2021-10-01T00:00:00+09:00"),
        ToDoRead(id=2, contents="할 일 내용2", is_done=True, created_at="2021-10-01T00:00:00+09:00", updated_at="2021-10-01T00:00:00+09:00")
    ]
    
    mocker.patch("fastapi_study.routers.todo.ToDoService.get_all_todos", return_value=mock_return_value)
    
    res = client.get("/todos")
    
    assert res.status_code == 200
    assert res.json() == [
        {
            "id": 1,
            "contents": "할 일 내용",
            "is_done": False,
            "created_at": "2021-10-01T00:00:00+09:00",
            "updated_at": "2021-10-01T00:00:00+09:00"
        },
        {
            "id": 2,
            "contents": "할 일 내용2",
            "is_done": True,
            "created_at": "2021-10-01T00:00:00+09:00",
            "updated_at": "2021-10-01T00:00:00+09:00"
        }
    ]
    
    
def test_get_todo_by_id(client: TestClient, mocker: MockerFixture):
    mock_return_value = ToDoRead(id=1, contents="할 일 내용", is_done=False, created_at="2021-10-01T00:00:00+09:00", updated_at="2021-10-01T00:00:00+09:00")
    
    mocker.patch("fastapi_study.routers.todo.ToDoService.get_todo_by_id", return_value=mock_return_value)
    
    res = client.get("/todos/1")
    
    assert res.status_code == 200
    assert res.json() == {
        "id": 1,
        "contents": "할 일 내용",
        "is_done": False,
        "created_at": "2021-10-01T00:00:00+09:00",
        "updated_at": "2021-10-01T00:00:00+09:00"
    }
    

def test_create_new_todo_success(client: TestClient, mocker: MockerFixture):
    user_input_value = {
        "contents": "할 일 내용",
        "is_done": False
    }
    mock_return_value = ToDoRead(id=1, contents="할 일 내용", is_done=True, created_at="2021-10-01T00:00:00+09:00", updated_at="2021-10-01T00:00:00+09:00")
    
    mock_create_new_todo = mocker.patch("fastapi_study.routers.todo.ToDoService.create_new_todo", return_value=mock_return_value)
    
    res = client.post("/todos", json=user_input_value)
    
    assert mock_create_new_todo.assert_called_once_with(ToDoCreate(**user_input_value)) is None
    
    assert res.status_code == 201
    assert res.json() == {
        "id": 1,
        "contents": "할 일 내용",
        "is_done": True,
        "created_at": "2021-10-01T00:00:00+09:00",
        "updated_at": "2021-10-01T00:00:00+09:00"
    }
