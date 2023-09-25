"""
/todos 하위 로직을 처리하는 라우터를 정의
"""

from typing import Annotated

from fastapi_study.database import get_db
from fastapi_study.schemas.todo import ToDoCreate, ToDoRead, ToDoUpdate
from fastapi_study.services.todo import ToDoService
from fastapi_study.core import exceptions

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import Body, Path, Query
from sqlalchemy.orm import Session

router = APIRouter()

@router.get(
    "",
    tags=["todo"],
    response_model=list[ToDoRead],
    summary="모든 ToDo 조회",
    description="DB에서 모든 ToDo를 조회합니다."
)
async def get_todos(
    todo_service: Annotated[ToDoService, Depends()]
):
    return todo_service.get_all_todos()

@router.post(
    "",
    tags=["todo"],
    response_model=ToDoRead,
    summary="새로운 ToDo 생성",
    description="새로운 ToDo를 생성합니다.",
    status_code=status.HTTP_201_CREATED,
)
async def create_todo(
    new_todo: ToDoCreate,
    todo_service: Annotated[ToDoService, Depends()]
):
    try:
        return todo_service.create_new_todo(new_todo)
    except exceptions.TodoNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get(
    "/{todo_id}",
    tags=["todo"],
    response_model=ToDoRead,
    summary="특정 ToDo 조회",
    description="특정 ToDo를 조회합니다."
)
async def get_todo(
    todo_id: Annotated[int, Path(..., description="조회할 todo id", ge=1)],
    todo_service: Annotated[ToDoService, Depends()]
):
    try:
        return todo_service.get_todo_by_id(todo_id)
    except exceptions.TodoNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.patch(
    "/{todo_id}",
    tags=["todo"],
    response_model=ToDoRead,
    summary="특정 ToDo 수정",
    description="특정 ToDo를 수정합니다."
)
async def update_todo(
    todo_id: Annotated[int, Path(..., description="변경할 todo id", ge=1)],
    update_todo_data: Annotated[ToDoUpdate, Body(..., description="변경할 todo 데이터", examples=[{"contents": "새로운 할 일 내용", "is_done": True}])],
    todo_service: Annotated[ToDoService, Depends()]
):
    try:
        return todo_service.update_todo(todo_id, update_todo_data)
    except exceptions.TodoNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete(
    "/{todo_id}",
    tags=["todo"],
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_todo(
    todo_id: Annotated[int, Path(..., description="삭제할 todo id", ge=1)],
    todo_service: Annotated[ToDoService, Depends()]
):
    try:
        todo_service.delete_todo_by_id(todo_id)
    except exceptions.TodoNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))