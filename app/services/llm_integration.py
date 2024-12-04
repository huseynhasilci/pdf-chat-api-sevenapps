import google.generativeai as genai
from app.config import GeminiAISettings
from app.constans.ApplicationConstants import MODEL_NAME


settings = GeminiAISettings()


class GeminiAIManager:

    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(MODEL_NAME)

    async def generate_pdf_content_response(self, pdf_content: str, message: str) -> str:
        response = self.model.generate_content([message, pdf_content])
        return response.text
