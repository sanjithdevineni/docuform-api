from pydantic import BaseModel
from datetime import datetime

class DocumentBase(BaseModel):
    filename: str
    file_type: str
    extracted_text: str | None = None

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: int
    upload_time: datetime

    class Config:
        orm_mode = True