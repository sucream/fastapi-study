"""
/todos 하위 로직을 처리하는 라우터를 정의
"""

from typing import Annotated

from fastapi_study.database import get_db
from fastapi_study.schemas.todo import ToDoCreate, ToDoRead, ToDoUpdate
from fastapi_study.schemas.errors import ErrorMsg
from fastapi_study.services import todo as todo_service

from fastapi import APIRouter, Depends, HTTPException
from fastapi import Body, Path, Query
from sqlalchemy.orm import Session

router = APIRouter()

@router.get(
    "",
    tags=["todo"],
    response_model=list[ToDoRead],
    responses={
        400: {
            "description": "잘못된 요청",
            "model": ErrorMsg,
        },
    }
)
async def get_todos(
    db: Annotated[Session, Depends(get_db)]
):
    return todo_service.get_all_todos(db)

@router.post(
    "",
    tags=["todo"],
    response_model=ToDoRead
)
async def create_todo(
    new_todo: ToDoCreate,
    db: Annotated[Session, Depends(get_db)]
):
    return todo_service.create_new_todo(new_todo, db)

@router.patch(
    "/{todo_id}",
    tags=["todo"],
    response_model=ToDoRead
)
async def update_todo(
    todo_id: Annotated[int, Path(...)],
    update_todo_data: Annotated[ToDoUpdate, Body(...)],
    db: Annotated[Session, Depends(get_db)]
):
    try:
        return todo_service.update_todo(todo_id, update_todo_data, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
