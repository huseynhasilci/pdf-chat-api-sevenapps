import io
from fastapi.testclient import TestClient
from main import app, MAX_FILE_SIZE_MB


client = TestClient(app)


def test_upload_pdf():
    test_file = 'tests/Setophaga_angelae.pdf'
    files = {'file': ('Setophaga_angelae.pdf', open(test_file, 'rb'))}
    response = client.post('/v1/pdf', files=files)
    assert response.status_code == 200
    assert response.json()['message'] == 'File uploaded successfully'


def test_upload_wrong_file():
    test_file = 'tests/test.txt'
    files = {'file': ('test.txt', open(test_file, 'rb'))}
    response = client.post('/v1/pdf', files=files)
    assert response.status_code == 500


def test_upload_file_over_limit():
    large_pdf_content = b"%PDF-1.4\n%Large Test PDF content" * 1024 * 1024
    large_pdf_file = io.BytesIO(large_pdf_content)

    response = client.post(
        "/v1/pdf",
        files={"file": ("large_file.pdf", large_pdf_file, "application/pdf")},
    )

    assert response.status_code == 500
    assert response.json() == {'detail': 'Upload failed413: File size exceeds 2 MB limit'}
