import os
from typing import Literal
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract
import docx

def allowed_file(filename: str) -> bool:
    allowed_extensions = {"pdf", "png", "jpg", "jpeg", "docx"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions

def get_file_type(filename: str) -> Literal["pdf", "image", "docx", "other"]:
    ext = filename.rsplit(".", 1)[1].lower()
    if ext == "pdf":
        return "pdf"
    elif ext in {"png", "jpg", "jpeg"}:
        return "image"
    elif ext == "docx":
        return "docx"
    else:
        return "other"

def extract_text(file_path: str, file_type: str) -> str:
    if file_type == "pdf":
        reader = PdfReader(file_path)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        return text
    elif file_type == "image":
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
        return text
    elif file_type == "docx":
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    else:
        return ""