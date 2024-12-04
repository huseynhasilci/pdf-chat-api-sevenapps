import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from main import app


client = TestClient(app)

mock_pdf_content = {"content": "This is a test PDF content."}
mock_ai_response = "This is a mock AI response."
mock_chat_id = "mock_chat_id_123"


@pytest.mark.asyncio
@patch("main.mongo_db_reference.read_pdf", new_callable=AsyncMock)
@patch("main.mongo_db_reference.save_chat", new_callable=AsyncMock)
@patch("main.geminiAI_reference.generate_pdf_content_response", new_callable=AsyncMock)
async def test_chat_with_ai_success(mock_generate_response, mock_save_chat, mock_read_pdf):
    # Mocking return values
    mock_read_pdf.return_value = mock_pdf_content
    mock_generate_response.return_value = mock_ai_response
    mock_save_chat.return_value = mock_chat_id

    pdf_id = "test_pdf_id"
    user_message = "Hello, AI!"

    response = client.post(f"/v1/chat/{pdf_id}?message={user_message}")

    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert data["chat_id"] == mock_chat_id
    assert data["pdf_id"] == pdf_id
    assert data["user_message"] == user_message
    assert data["model_response"] == mock_ai_response

    mock_read_pdf.assert_called_once_with(pdf_id)
    mock_generate_response.assert_called_once_with(mock_pdf_content["content"], user_message)
    mock_save_chat.assert_called_once_with(
        pdf_id=pdf_id,
        user_message=user_message,
        llm_response=mock_ai_response
    )


@pytest.mark.asyncio
@patch("main.mongo_db_reference.read_pdf", new_callable=AsyncMock)
async def test_chat_with_ai_pdf_not_found(mock_read_pdf):

    mock_read_pdf.return_value = None

    pdf_id = "nonexistent_pdf_id"
    user_message = "Hello, AI!"

    response = client.post(f"/v1/chat/{pdf_id}?message={user_message}")

    assert response.status_code == 400
    assert response.json() == {'error': 'PDF not found'}

    mock_read_pdf.assert_called_once_with(pdf_id)


@pytest.mark.asyncio
@patch("main.mongo_db_reference.read_pdf", new_callable=AsyncMock)
@patch("main.geminiAI_reference.generate_pdf_content_response", new_callable=AsyncMock)
async def test_chat_with_ai_ai_failure(mock_generate_response, mock_read_pdf):
    mock_read_pdf.return_value = mock_pdf_content

    pdf_id = "test_pdf_id"
    user_message = "Hello, AI!"

    response = client.post(f"/v1/chat/{pdf_id}?message={user_message}")

    assert response.status_code == 500

    mock_read_pdf.assert_called_once_with(pdf_id)
    mock_generate_response.assert_called_once_with(mock_pdf_content["content"], user_message)
