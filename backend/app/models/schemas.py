from pydantic import BaseModel
from typing import Optional

class ProcessorResponse(BaseModel):
    success: bool
    message: str
    filename: Optional[str] = None
    download_url: Optional[str] = None

class ErrorResponse(BaseModel):
    detail: str

class HealthResponse(BaseModel):
    status: str
