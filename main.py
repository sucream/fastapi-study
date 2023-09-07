from fastapi_study.database import create_all_tables, get_db
from fastapi_study.schemas.todo import ToDoCreate, ToDoRead
from fastapi_study.schemas.errors import ErrorMsg
from fastapi_study.services.todo import get_all_todos, create_new_todo

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session


create_all_tables()
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get(
    "/todos",
    tags=["todo"],
    response_model=list[ToDoRead],
    responses={
        400: {
            "description": "잘못된 요청",
            "model": ErrorMsg,
        },
    }
)
async def get_todos(db: Session=Depends(get_db)):
    return get_all_todos(db)

@app.post(
    "/todos",
    tags=["todo"],
    response_model=ToDoRead
)
async def create_todo(new_todo: ToDoCreate, db: Session=Depends(get_db)):
    return create_new_todo(new_todo, db)