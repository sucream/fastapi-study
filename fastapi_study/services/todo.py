from typing import Annotated
import logging


from fastapi_study.models.todo import ToDo as ToDoModel
from fastapi_study.schemas.todo import ToDoCreate as ToDoCreateSchema
from fastapi_study.schemas.todo import ToDoUpdate as ToDoUpdateSchema
from fastapi_study.core import exceptions
from fastapi_study.database import get_db

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session


class ToDoService:
    """
    ToDo 관련 비즈니스 로직을 담당하는 클래스
    """
    
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        self.db = db
        
        
    def get_all_todos(self) -> list[ToDoModel]:
        """
        모든 ToDo를 조회합니다.
        
        Parameters
        ----------
            
        Returns
        -------
        list[ToDoModel]
            모든 ToDo
        """
        
        stmt = select(ToDoModel)
        return self.db.scalars(stmt).all()

    def get_todo_by_id(self, todo_id: int) -> ToDoModel:
        """
        특정 ToDo를 조회합니다.
        
        Parameters
        ----------
        todo_id : int
            조회할 ToDo의 ID
            
        Returns
        -------
        ToDoModel
            특정 ToDo
        """
        
        stmt = select(ToDoModel).where(ToDoModel.id == todo_id)
        todo = self.db.scalar(stmt)
        if todo is None:
            raise exceptions.TodoNotFoundError(f"Todo {todo_id} is not exists")
        return todo

    def create_new_todo(
        self,
        new_todo: ToDoCreateSchema,
    ) -> ToDoModel:
        """
        새로운 ToDo를 생성합니다.
        
        Parameters
        ----------
        new_todo : ToDoCreate
            새로운 ToDo
            
        Returns
        -------
        ToDoModel
            새로 생성된 ToDo
        """
        logging.info(f"똑똑{new_todo}")
        todo = ToDoModel(**new_todo.model_dump())
        self.db.add(todo)
        self.db.commit()
        self.db.refresh(todo)
        return todo

    def update_todo(
        self,
        todo_id: int,
        update_todo_data: ToDoUpdateSchema,
    ) -> ToDoModel:
        """
        기존의 ToDo를 수정합니다.
        
        Parameters
        ----------
        todo_id : int
            수정할 ToDo의 ID
        update_todo_data : ToDoUpdate
            수정할 ToDo
            
        Returns
        -------
        ToDoModel
            수정된 ToDo
        """
        
        get_exist_todo_query = select(ToDoModel).where(ToDoModel.id == todo_id)
        
        # 수정할 ToDo가 존재하는지 확인
        todo = self.db.scalar(get_exist_todo_query)
        if todo is None:
            raise exceptions.TodoNotFoundError(f"Todo {todo_id} is not exists")
        
        # 수정할 내용을 반영
        for key, value in update_todo_data.model_dump(exclude_unset=True).items():
            print(key, value)
            setattr(todo, key, value)
        
        self.db.commit()
        self.db.refresh(todo)
        return todo

    def delete_todo_by_id(
        self,
        todo_id: int,
    ):
        """
        기존의 ToDo를 삭제합니다.
        
        Parameters
        ----------
        todo_id : int
            삭제할 ToDo의 ID
        """
        
        get_exist_todo_query = select(ToDoModel).where(ToDoModel.id == todo_id)
        
        # 삭제할 ToDo가 존재하는지 확인
        todo = self.db.scalar(get_exist_todo_query)
        if todo is None:
            raise exceptions.TodoNotFoundError(f"Todo {todo_id} is not exists")
        
        self.db.delete(todo)
        self.db.commit()