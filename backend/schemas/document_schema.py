from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: int 
    filename : str
    content_type : str


class DocumentUpdate(BaseModel):
    filename : str
    content_type : str