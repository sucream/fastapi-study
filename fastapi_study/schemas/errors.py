from pydantic import BaseModel, Field, ConfigDict


class ErrorMsg(BaseModel):
    error_code: int = Field(..., description="에러 코드")
    simple_msg: str = Field(..., description="간단한 에러 메시지")
    detail_msg: str = Field(..., description="자세한 에러 메시지")