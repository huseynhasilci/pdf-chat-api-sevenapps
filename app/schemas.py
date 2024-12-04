from pydantic import BaseModel
from typing import Optional

from datetime import datetime


class PDFUploadResponseSchema(BaseModel):
    file_id: str
    filename: str
    page_count: int
    message: str


class ChatResponseSchema(BaseModel):
    chat_id: str
    pdf_id: str
    user_message: str
    model_response: str
    created_at: Optional[datetime] = datetime.utcnow()

    class Config:
        from_attributes = True
