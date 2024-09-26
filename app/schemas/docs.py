from pydantic import BaseModel


class DocsPost(BaseModel):
    contents: str


class DocsPut(BaseModel):
    contents: str
