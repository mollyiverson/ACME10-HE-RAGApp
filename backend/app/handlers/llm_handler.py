import os
import pandas as pd
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
from transformers import pipeline
from backend.app.handlers.vector_search_handler import VectorSearchHandler

##############################################################
### TODO: USE IMPORTS WHEN CONFIG FILE IS CORRECTLY SET UP ###
##############################################################
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

# OpenAI Configuration
load_dotenv()  # Loads variables from .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Store API Key in Environment Variable
CHATGPT_MODEL = "gpt-4o-mini"  # Use GPT-4o-mini for efficiency

# LLM Model for CI environment
LLM_MODEL_NAME = "distilgpt2" if os.getenv("CI") else None  # DistilBERT LLM to save memory in automated testing

class LLMHandler:
    def __init__(self, embedding_path=EMBEDDINGS_FILE):
        """
        Initialize the LLM handler with OpenAI ChatGPT model and vector search handler.
        """
        if os.getenv("CI"):
            self.llm = pipeline("text-generation", model=LLM_MODEL_NAME)
        else:
            if not OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY environment variable not set")
            self.client = OpenAI(api_key=OPENAI_API_KEY)  # Initialize OpenAI Client
        self.vector_search_handler = VectorSearchHandler(embedding_path=embedding_path)

    def get_vector_search_results(self, query_vector, top_k=10):
        """
        Perform vector search and retrieve top-k vector results.
        """
        similarities, indices = self.vector_search_handler.search(query_vector, top_k=top_k)
        return {"similarities": similarities, "indices": indices}

    def format_query(self, original_query, vector_search_text_results, kg_output):
        """
        Combine VS and KG outputs into a single natural-language query.
        """
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
            - Use the information from the vector search results and the knowledge graph context, if they exist, to provide a concise and accurate response to the query.
            - Avoid repeating the input query in your response.
            - Provide only relevant information that answers the query directly.
            - If you couldn't find relevant information from the vector search results or the knowledge graph, try to answer on your own and state how you didn't have additional context.
        """
        return query

    def query_llm(self, query, max_tokens=200, temperature=0.5):
        if os.getenv("CI"):
            response = self.llm(query, max_new_tokens=max_tokens, temperature=temperature, do_sample=True)
            full_text = response[0]["generated_text"]
            llm_response = full_text[len(query):].strip()
            return llm_response
        else:
            try:
                response = self.client.chat.completions.create(
                    model=CHATGPT_MODEL,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": query}
                    ],
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                print(f"Error querying ChatGPT: {e}")
                return "An error occurred while generating a response."


# Example Usage
if __name__ == "__main__":
    # Initialize LLM handler
    llm_handler = LLMHandler()

    # Load dataset embeddings
    embeddings = llm_handler.vector_search_handler.load_embeddings()
    
    # Build a vector index and load
    llm_handler.vector_search_handler.build_index(embeddings)

    example_query_text = "What is the requirements engineering book about?"
    example_query_vector = llm_handler.vector_search_handler.embed_query(example_query_text)

    # Perform vector search on query vector and embeddings dataset
    vector_search_results = llm_handler.vector_search_handler.search(example_query_vector)
    similarities, indices = vector_search_results
    
    # Get texts based on VS indices
    vector_search_texts = llm_handler.vector_search_handler.get_search_results(indices)
    
    # Mock knowledge graph output
    kg_output = "Alan Turing developed the idea of the Turing machine."

    # Format query and get LLM response
    query = llm_handler.format_query(example_query_text, vector_search_texts, kg_output)
    print("Query to LLM:\n", query)

    response = llm_handler.query_llm(query)
    print("LLM Response:\n", response)