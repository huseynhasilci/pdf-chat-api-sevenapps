from app.services.pdf_extractor import decompress_pdf_content_bytes
from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId
from app.models import PDFDocument, ChatMessage


class MongoDBCrudOperations:

    def __init__(self, uri: str, db_name: str, collection_name: str):
        self.uri = uri
        self.db_name = db_name
        self.collection_name = collection_name

        self.client = AsyncIOMotorClient(self.uri)
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]

    async def create_pdf(self, filename: str, content: bytes, page_count: int) -> str:  # , content_as_byte: bytes
        pdf_document_dict = {
            "filename": filename,
            "content": content,
            "page_count": page_count,
        }

        pdf_document = PDFDocument(**pdf_document_dict)
        print("pdf_document_dict", pdf_document)
        # result = await self.collection.insert_one(pdf_document)
        result = await self.db.pdf_files.insert_one(pdf_document.dict(by_alias=True))

        return str(result.inserted_id)

    async def read_pdf(self, pdf_id: str) -> dict:
        # pdf = await self.collection.find_one({"_id": ObjectId(pdf_id)})
        pdf = await self.db.pdf_files.find_one({"_id": ObjectId(pdf_id)})

        if pdf:
            decompressed_content = await decompress_pdf_content_bytes(pdf["content"])
            return {"content": decompressed_content}
        return {}

    async def save_chat(self, pdf_id: str, user_message: str, llm_response: str) -> str:
        chat_msg = ChatMessage(
            pdf_id=pdf_id,
            user_message=user_message,
            model_response=llm_response
        )

        result = await self.db.chat.insert_one(chat_msg.dict(by_alias=True))

        return str(result.inserted_id)

    async def close(self) -> None:
        if self.client:
            self.client.close()
