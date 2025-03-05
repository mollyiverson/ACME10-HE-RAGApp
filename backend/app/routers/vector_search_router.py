from fastapi import APIRouter, HTTPException
from app.handlers.vector_search_handler import VectorSearchHandler
from app.models.vector_search_query import VectorSearchQuery

router = APIRouter()

@router.post("/search")
def vector_search(search_query: VectorSearchQuery):
    """
    Perform a vector search using the provided query text.
    :param search_query: <SearchQuery> The input query and optional top_k parameter.
    :return: <dict> The search results, including similarities and matched texts.
    """
    try:
        print(f"Received search query: {search_query}")

        vector_handler = VectorSearchHandler()
        
        # Ensure embeddings and index are loaded at startup
        try:
            vector_handler.load_embeddings()
            vector_handler.load_index()
        except Exception as e:
            print(f"Error loading vector search handler: {e}")

        # Embed the query text
        query_vector = vector_handler.embed_query(search_query.query_text)
        
        # Perform the search
        similarities, indices = vector_handler.search(query_vector, top_k=search_query.top_k)

        # Retrieve search results
        search_results = vector_handler.get_search_results(indices)

        # Return the results in a structured format
        return {
            "query": search_query.query_text,
            "top_k": search_query.top_k,
            "results": [
                {"text": text, "similarity": float(similarity)}  # Explicitly convert to Python float
                for text, similarity in zip(search_results, similarities)
            ],
        }
    
    except Exception as e:
        print(f"Detailed error in vector search: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error in vector search: {str(e)}")
