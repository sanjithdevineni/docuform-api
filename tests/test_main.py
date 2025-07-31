import os
import shutil
import tempfile
from fastapi.testclient import TestClient
from app.main import app, UPLOAD_DIR

def setup_module(module):
    # Ensure uploads dir is clean before tests
    if os.path.exists(UPLOAD_DIR):
        shutil.rmtree(UPLOAD_DIR)
    os.makedirs(UPLOAD_DIR)

def teardown_module(module):
    # Clean up uploads dir after tests
    if os.path.exists(UPLOAD_DIR):
        shutil.rmtree(UPLOAD_DIR)

client = TestClient(app)

def test_index_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "Click or drag a file here to upload" in response.text

def test_upload_and_list_document():
    # Create a temporary text file to upload as a docx
    tmp_dir = tempfile.mkdtemp()
    docx_path = os.path.join(tmp_dir, "test.docx")
    from docx import Document
    doc = Document()
    doc.add_paragraph("Hello, this is a test docx file.")
    doc.save(docx_path)
    with open(docx_path, "rb") as f:
        response = client.post("/upload", files={"file": ("test.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")})
    assert response.status_code in (200, 303)
    # Now check if the document appears in the list
    response = client.get("/")
    assert "test.docx" in response.text
    assert "Hello, this is a test docx file." in response.text
    shutil.rmtree(tmp_dir)