import pandas as pd
import numpy as np
from vector_search_handler import VectorSearchHandler
from transformers import pipeline

class LLMHandler:
    def __init__(self, model_name="meta-llama/Llama-2-7b-chat-hf",
                 embedding_path="embeddings_output/text_embeddings.npy"):
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
        formatted_vs_results = "\n".join([f"- {result}" for result in vector_search_text_results])

        query = f"""
            Question: {original_query}

            Context from vector search results based on the query:
            {formatted_vs_results}

            Context from the knowledge graph based on the query:
            "{kg_output}"
        """
        
        return query


    def query_llm(self, query, max_new_tokens=300, temperature=0.7):
        """
        Query the LLM and return a formatted response.
        """
        response = self.llm(query, max_new_tokens=max_new_tokens,
                            temperature=temperature, do_sample=True)
        
        return response[0]["generated_text"]


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
