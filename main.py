import logging
from app.schemas import ChatResponseSchema, PDFUploadResponseSchema
from app.middlewares.error_handling import CustomErrorHandlingMiddleware
from app.services.llm_integration import GeminiAIManager
from fastapi import FastAPI, File, UploadFile, HTTPException
from app.crud import MongoDBCrudOperations
from app.services.pdf_extractor import extract_text
from app.config import (
    MongoSettings
)

MAX_FILE_SIZE_MB = 2
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
UPLOAD_TIMEOUT_SECONDS = 30

settings = MongoSettings()
geminiAI_reference = GeminiAIManager()

mongo_db_reference = MongoDBCrudOperations(
    uri=settings.DATABASE_URL,
    db_name=settings.DATABASE_NAME,
    collection_name=settings.COLLECTION_NAME
)

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)
app = FastAPI()

# app.add_middleware(CustomErrorHandlingMiddleware)


@app.post("/v1/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:

        if not file.content_type.endswith('pdf'):
            raise HTTPException(status_code=500, detail='File type not supported')

        if file.size > MAX_FILE_SIZE_BYTES:
            raise HTTPException(status_code=413, detail=f'File size exceeds {MAX_FILE_SIZE_MB} MB limit')

        file_content = await extract_text(file)
        file_id = await mongo_db_reference.create_pdf(
            file.filename,
            file_content.get('compressed_text'),
            file_content.get('page_count'),
        )

        return PDFUploadResponseSchema(
            file_id=file_id,
            filename=file.filename,
            page_count=file_content.get('page_count'),
            message="File uploaded successfully",
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed{str(e)}")


@app.post("/v1/chat/{pdf_id}")
async def chat_with_ai(pdf_id: str, message: str):
    try:
        pdf_content = await mongo_db_reference.read_pdf(pdf_id)

        if not pdf_content:
            raise HTTPException(status_code=500, detail=f"PDF not found")

        response = geminiAI_reference.generate_pdf_content_response(pdf_content.get('content'), message)

        chat_id = await mongo_db_reference.save_chat(
            pdf_id=pdf_id,
            user_message=message,
            llm_response=response,
        )

        return ChatResponseSchema(
            chat_id=chat_id,
            pdf_id=pdf_id,
            user_message=message,
            model_response=response
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong {str(e)}")
