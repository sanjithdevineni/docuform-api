from fastapi import FastAPI, Request, UploadFile, File, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import shutil
import os

from . import models, schemas, crud, utils, database

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
UPLOAD_DIR = "app/uploads"

models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    documents = crud.get_documents(db)
    return templates.TemplateResponse("index.html", {"request": request, "documents": documents})

@app.post("/upload")
def upload_document(request: Request, file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not utils.allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="Unsupported file type.")
    file_type = utils.get_file_type(file.filename)
    save_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    extracted_text = utils.extract_text(save_path, file_type)
    doc_in = schemas.DocumentCreate(
        filename=file.filename,
        file_type=file_type,
        extracted_text=extracted_text
    )
    crud.create_document(db, doc_in)
    return RedirectResponse(url="/", status_code=303)

@app.get("/documents/{doc_id}", response_class=HTMLResponse)
def view_document(doc_id: int, request: Request, db: Session = Depends(get_db)):
    document = crud.get_document(db, doc_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return templates.TemplateResponse("index.html", {"request": request, "documents": [document]})