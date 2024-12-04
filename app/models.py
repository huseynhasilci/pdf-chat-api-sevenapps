from typing import Optional
from pydantic import BaseModel
from bson import ObjectId
from datetime import datetime


class PDFDocument(BaseModel):
    filename: str
    content: bytes
    page_count: int
    uploaded_at: Optional[datetime] = datetime.utcnow()

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class ChatMessage(BaseModel):
    pdf_id: str
    user_message: str
    model_response: str
    created_at: Optional[datetime] = datetime.utcnow()

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
