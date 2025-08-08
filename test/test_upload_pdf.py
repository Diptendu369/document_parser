import os
import shutil
from httpx import AsyncClient
import pytest
from app.main import app

# Clean up after tests
@pytest.fixture(autouse=True)
def cleanup_data_folder():
    yield
    data_folder = "data"
    for f in os.listdir(data_folder):
        if f.endswith(".pdf"):
            os.remove(os.path.join(data_folder, f))


@pytest.mark.asyncio
async def test_upload_pdf():
    test_file_path = "sample_test_file.pdf"

    # Create a dummy PDF file for testing
    with open(test_file_path, "wb") as f:
        f.write(b"%PDF-1.4 test file content")

    async with AsyncClient(app=app, base_url="http://test") as client:
        with open(test_file_path, "rb") as pdf_file:
            response = await client.post(
                "/upload-pdf",
                files={"file": ("sample_test_file.pdf", pdf_file, "application/pdf")}
            )

    # Check response
    assert response.status_code == 200
    assert "filename" in response.json()
    assert response.json()["filename"] == "sample_test_file.pdf"

    # Check file is saved
    saved_path = os.path.join("data", "sample_test_file.pdf")
    assert os.path.exists(saved_path)

    # Cleanup test file
    os.remove(test_file_path)
