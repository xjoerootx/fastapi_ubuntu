from datetime import date

from pydantic import BaseModel


class DocumentsAdd(BaseModel):
    path: str
    date: date


class DocumentstextAdd(BaseModel):
    id: int
    id_doc: int
    text: str

