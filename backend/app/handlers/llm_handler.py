import os
import pandas as pd
import numpy as np
from transformers import pipeline
from vector_search_handler import VectorSearchHandler
##############################
### TODO: FIX IMPORT ERROR ###
##############################
#from backend.app.config import EMBEDDINGS_FILE

### CONFIGS ###
# Configuration
# Base directory for data processing
# Get the absolute path to the current file's directory
CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
# Go up one level to the app directory
APP_DIR = os.path.dirname(CURRENT_FILE_DIR)
# Go up another level to the backend directory
BACKEND_DIR = os.path.dirname(APP_DIR)
# Go up another level to the root directory (if needed)
ROOT_DIR = os.path.dirname(BACKEND_DIR)
# Base directory for data processing
BASE_DATA_DIR = os.path.join(BACKEND_DIR, 'app', 'data_processing')

# Subdirectories for specific handlers
EMBEDDINGS_DATA_DIR = os.path.join(BASE_DATA_DIR, "embeddings_data")
VECTOR_SEARCH_DATA_DIR = os.path.join(BASE_DATA_DIR, "vector_search_data")
LLM_DATA_DIR = os.path.join(BASE_DATA_DIR, "llm_data")

# Common file paths
WIKI_DATA_FILE = os.path.join(BASE_DATA_DIR, "simpleWikiData.parquet")
CLEAN_WIKI_DATA_FILE = os.path.join(EMBEDDINGS_DATA_DIR, "clean_wiki_data.parquet")
EMBEDDINGS_FILE = os.path.join(EMBEDDINGS_DATA_DIR, "text_embeddings.npy")
FAISS_INDEX_FILE = os.path.join(VECTOR_SEARCH_DATA_DIR, "index.faiss")

class LLMHandler:
    def __init__(self, model_name="meta-llama/Llama-2-7b-chat-hf",
                 embedding_path=EMBEDDINGS_FILE):
        """
        Initialize the LLM handler with a specified model and vector search handler.
        """
        self.llm = pipeline("text-generation", model=model_name)
        self.vector_search_handler = VectorSearchHandler(
            embedding_path=embedding_path)

    def get_vector_search_results(self, query_vector, top_k=5):
        """
        Perform vector search and retrieve top-k vector results.
        """

        similarities, indices = self.vector_search_handler.search(
            query_vector, top_k=top_k)
        
        return {"similarities": similarities, "indices": indices}
    
    def format_query(self, original_query, vector_search_text_results, kg_output):
        """
        Combine VS and KG outputs into a single natural-language query.
        """
        # Join the array of vector search results with newlines
        # Handle empty or missing results gracefully
        formatted_vs_results = (
            "\n".join([f"- {result}" for result in vector_search_text_results])
            if vector_search_text_results else "No relevant vector search results were found."
        )
        
        formatted_kg_output = (
            f"Additional context: {kg_output}" if kg_output else "No additional context available from the knowledge graph."
        )
        
        query = f"""
            Query:
            {original_query}
            
            Vector Search Results:
            {formatted_vs_results}
            
            Knowledge Graph Context:
            {formatted_kg_output}
        
            Instructions:
            - Use the information from the vector search results and the knowledge graph context to provide a concise and accurate response to the query.
            - Avoid repeating the input query in your response.
            - Provide only relevant information that answers the query directly.
        """
        return query
    
    def query_llm(self, query, max_new_tokens=200, temperature=0.5):
        """
        Generate a response from the LLM, excluding the prompt tokens.
        """
        # Generate the response with the pipeline
        response = self.llm(query,
                            max_new_tokens=max_new_tokens,
                            temperature=temperature,
                            do_sample=True)

        # Extract generated text and remove the prompt part
        full_text = response[0]["generated_text"]

        # Use tokenized length to slice off the prompt from the full text
        generated_text = full_text[len(query):].strip()  # Remove the exact query text

        return generated_text


# Example Usage
if __name__ == "__main__":
    # Initialize LLM handler
    llm_handler = LLMHandler()

    # Load dataset embeddings
    embeddings = llm_handler.vector_search_handler.load_embeddings()
    
    # Build a vector index and load
    llm_handler.vector_search_handler.build_index(embeddings)

    #example_query_vector = np.expand_dims(embeddings[0], axis=0)    
    example_query_text = "Who is Alan Turing?"
    example_query_vector = llm_handler.vector_search_handler.embed_query(example_query_text)

    # Perform vector search on query vector and embeddings dataset
    vector_search_results = llm_handler.vector_search_handler.search(example_query_vector)
    similarities, indices = vector_search_results
    
    # Get texts based on VS indices
    vector_search_texts = llm_handler.vector_search_handler.get_search_results(indices)
    
    # Mock knowledge graph output
    kg_output = "Alan Turing developed the idea of the turing machine."

    # Format query and get LLM response
    query = llm_handler.format_query(example_query_text, vector_search_texts, kg_output)
    print("Query to LLM:\n", query)

    response = llm_handler.query_llm(query)
    print("LLM Response:\n", response)