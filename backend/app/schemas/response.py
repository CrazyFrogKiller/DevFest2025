from pydantic import BaseModel


class ResponseSchema(BaseModel):
    """Base response schema"""
    success: bool
    message: str
    data: dict = {}


class ErrorResponse(BaseModel):
    """Error response schema"""
    success: bool = False
    message: str
    error_code: Optional[str] = None
