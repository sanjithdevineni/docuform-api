# docuform-api

A minimal FastAPI web app for uploading, extracting, and viewing text from PDF, image, and DOCX files. Uploaded files and extracted text are stored in a SQLite database. The app features a simple, modern web UI.

## Features
- Upload PDF, image (PNG, JPG, JPEG), or DOCX files
- Extracts and displays text from uploaded documents
- Stores file metadata and extracted text in SQLite
- Simple, responsive web interface with drag-and-drop upload

## Requirements
- Python 3.8+
- pip (Python package manager)

## Setup
1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd docuform-api
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the App
1. **Start the FastAPI server:**
   ```bash
   uvicorn app.main:app --reload
   ```
2. **Open your browser and visit:**
   [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Usage
- Click or drag a file into the upload area to select a document.
- Click "Upload" to process the file and view the extracted text below.
- Uploaded documents and their extracted text will be listed on the main page.

## Running Tests
To run the automated tests:
```bash
PYTHONPATH=. pytest
```

## Notes
- Uploaded files are stored in `app/uploads/` and metadata in `app.db` (SQLite).
- For production, consider using a more robust database and deploying behind a reverse proxy (see deployment notes in previous responses).
- The UI is designed for simplicity and ease of use.

---
