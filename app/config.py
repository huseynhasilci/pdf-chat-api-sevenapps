import os
from app.constans.EnvConstants import (
    GEMINI_API_KEY,
    DATABASE_URL,
    DATABASE_NAME,
    COLLECTION_NAME,
    ELASTICSEARCH_HOTS
)
from dotenv import load_dotenv

load_dotenv()


class GeminiAISettings:
    GEMINI_API_KEY: str = os.getenv(GEMINI_API_KEY)


class MongoSettings:
    DATABASE_URL: str = os.getenv(DATABASE_URL)
    DATABASE_NAME: str = os.getenv(DATABASE_NAME)
    COLLECTION_NAME: str = os.getenv(COLLECTION_NAME)


class ElasticSearchSettings:
    ELASTICSEARCH_HOTS: str = os.getenv(ELASTICSEARCH_HOTS)
