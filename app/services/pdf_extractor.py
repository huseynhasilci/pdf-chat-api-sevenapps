import PyPDF2
from io import BytesIO
import zlib
from fastapi import UploadFile


async def extract_text(file: UploadFile) -> dict:  # bytes:
    pdf_reader = PyPDF2.PdfReader(BytesIO(await file.read()))

    page_counter = len(pdf_reader.pages)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""

    file_content = {
        "page_count": page_counter,
        "compressed_text": zlib.compress(text.encode("utf-8"))
    }

    return file_content  # zlib.compress(text.encode("utf-8"))


async def decompress_pdf_content_bytes(input_bytes: bytes) -> str:
    return zlib.decompress(input_bytes).decode("utf-8")
