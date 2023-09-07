from fastapi_study.models.todo import ToDo as ToDoModel
from fastapi_study.schemas.todo import ToDoCreate as ToDoCreateSchema


from sqlalchemy import select
from sqlalchemy.orm import Session


def get_all_todos(db: Session) -> list[ToDoModel]:
    """
    모든 ToDo를 조회합니다.
    
    Parameters
    ----------
    db : Session
        DB 세션
        
    Returns
    -------
    list[ToDoModel]
        모든 ToDo
    """
    
    stmt = select(ToDoModel)
    return db.scalars(stmt).all()


def create_new_todo(
    new_todo: ToDoCreateSchema,
    db: Session
) -> ToDoModel:
    """
    새로운 ToDo를 생성합니다.
    
    Parameters
    ----------
    new_todo : ToDoCreateSchema
        새로운 ToDo
    db : Session
        DB 세션
        
    Returns
    -------
    ToDoModel
        새로 생성된 ToDo
    """
    
    todo = ToDoModel(**new_todo.model_dump())
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo