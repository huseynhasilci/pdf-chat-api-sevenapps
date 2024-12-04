from app.schemas import ChatResponseSchema, PDFUploadResponseSchema
from app.middlewares.error_handling import CustomErrorHandlingMiddleware
from app.services.llm_integration import GeminiAIManager
from fastapi import FastAPI, File, UploadFile
from app.crud import MongoDBCrudOperations
from app.services.pdf_extractor import extract_text
from app.config import (
    MongoSettings
)
from app.exceptions.exceptions import (
    FileTypeNotSupportedError,
    FileSizeExceedError,
    PDFNotFoundError,
)

MAX_FILE_SIZE_MB = 5
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
UPLOAD_TIMEOUT_SECONDS = 30

settings = MongoSettings()
geminiAI_reference = GeminiAIManager()

mongo_db_reference = MongoDBCrudOperations(
    uri=settings.DATABASE_URL,
    db_name=settings.DATABASE_NAME,
    collection_name=settings.COLLECTION_NAME
)

app = FastAPI()

app.add_middleware(CustomErrorHandlingMiddleware)


@app.post("/v1/pdf")
async def upload_pdf(file: UploadFile = File(...)):

    if not file.content_type.endswith('pdf'):
        raise FileTypeNotSupportedError(
            status_code=400,
            message='File type not supported',
            name="File Type Error"
        )

    if file.size > MAX_FILE_SIZE_BYTES:
        raise FileSizeExceedError(
            status_code=400,
            message=f'File size exceeds {MAX_FILE_SIZE_MB} MB limit',
            name="File Size Exceed Error",
        )

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


@app.post("/v1/chat/{pdf_id}")
async def chat_with_ai(pdf_id: str, message: str):

    pdf_content = await mongo_db_reference.read_pdf(pdf_id)

    if not pdf_content:
        raise PDFNotFoundError(
            status_code=500,
            message=f'PDF not found',
            name="PDF Not Found Error",
        )

    response = await geminiAI_reference.generate_pdf_content_response(pdf_content.get('content'), message)

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
