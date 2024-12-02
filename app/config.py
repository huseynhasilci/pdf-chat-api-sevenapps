import os
from dotenv import load_dotenv

load_dotenv()


class GeminiAISettings:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")


class MongoSettings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME")
    COLLECTION_NAME: str = os.getenv("COLLECTION_NAME")
