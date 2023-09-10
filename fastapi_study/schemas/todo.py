from pydantic import BaseModel, Field, ConfigDict


class TodoBase(BaseModel):
    """
    ToDo의 공통 스키마
    """
    contents: str = Field(..., max_length=256, description="할 일 내용")
    is_done: bool = Field(False, description="완료 여부")
    

class ToDoRead(TodoBase):
    """
    어플리케이션에서 사용할 ToDo 스키마
    """
    id: int = Field(..., description="고유 id")
    
    # pydantic 2.0 이후로는 Config 클래스를 사용하지 않고 ConfigDict를 사용
    model_config = ConfigDict(from_attributes=True)
    

class ToDoCreate(TodoBase):
    """
    ToDo 생성 시 사용할 스키마
    """
    pass

    model_config = ConfigDict(json_schema_extra={"examples": [{"contents": "할 일 내용", "is_done": False}]})


class ToDoUpdate(TodoBase):
    """
    ToDo 수정 시 사용할 스키마
    """
    contents: str|None = None
    is_done: bool|None = None
    
    model_config = ConfigDict(json_schema_extra={"examples": [{"contents": "할 일 내용", "is_done": False}, {"contents": "할 일 내용"}, {"is_done": True}]})