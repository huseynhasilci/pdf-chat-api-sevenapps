from app.services.pdf_extractor import decompress_pdf_content_bytes
from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId


class MongoDBCrudOperations:

    def __init__(self, uri: str, db_name: str, collection_name: str):
        self.uri = uri
        self.db_name = db_name
        self.collection_name = collection_name

        self.client = AsyncIOMotorClient(self.uri)
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]

    async def create_pdf(self, filename: str, content: bytes, page_count: int) -> str:  # , content_as_byte: bytes
        pdf_document = {
            "filename": filename,
            "content": content,
            "page_count": page_count,
        }
        result = await self.collection.insert_one(pdf_document)

        return str(result.inserted_id)

    async def read_pdf(self, pdf_id: str) -> dict:
        pdf = await self.collection.find_one({"_id": ObjectId(pdf_id)})
        print(pdf)
        if pdf:
            decompressed_content = await decompress_pdf_content_bytes(pdf["content"])
            return {"content": decompressed_content}
        return {}

    async def close(self) -> None:
        if self.client:
            self.client.close()
