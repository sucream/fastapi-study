from fastapi_study.database import create_all_tables, get_db
from fastapi_study.routers.todo import router as todo_router

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles  # static 파일 serving을 위한 모듈

create_all_tables()
app = FastAPI()

# /todos로 시작하는 경로는 todo_router로 처리하도록 위임
app.include_router(todo_router, prefix="/todos")

app.mount("/", StaticFiles(directory="public", html = True), name="static")


