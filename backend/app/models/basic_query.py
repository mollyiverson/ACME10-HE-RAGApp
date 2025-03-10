from pydantic import BaseModel
from typing import Optional, List

class Query(BaseModel):
    query: str
    vector_search_results: Optional[List[str]] = None
    kg_results: Optional[str] = None