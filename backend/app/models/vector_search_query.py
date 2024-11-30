from pydantic import BaseModel

class VectorSearchQuery(BaseModel):
    query_text: str
    top_k: int = 5  # Default value for top_k