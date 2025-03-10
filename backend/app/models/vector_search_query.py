from pydantic import BaseModel

class VectorSearchQuery(BaseModel):
    query_text: str
