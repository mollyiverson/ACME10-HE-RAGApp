import pandas as pd
import numpy as np
from vector_search_handler import VectorSearchHandler
from transformers import pipeline

TEXT_COLUMN = "text"  # Replace with the name of the column containing text

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

        distances, indices = self.vector_search_handler.search(
            query_vector, top_k=top_k)
        
        print(f"Distances, Indices: {distances, indices}")

        return {"distances": distances, "indices": indices}
    
    def get_documents_by_indices(self, indices, texts_path="embeddings_output/clean_wiki_data.parquet"):
        """
        Get the documents or data associated with the given indices.
        """
        original_data = pd.read_parquet(texts_path)
        selected_texts = original_data.iloc[indices[0]][TEXT_COLUMN].tolist()

        return selected_texts

    def format_query(self, original_query, vector_search_text_results, kg_output):
        """
        Combine VS and KG outputs into a single natural-language query.
        """
        query = f"""
        Original user query: {original_query}

        I performed a vector search and retrieved the following relevant texts to the original query:
        {vector_search_text_results}
                
        Additionally, the knowledge graph provides the following context:
        "{kg_output}"
    
        Use the vector search results consisting of relevant texts and the knowledge graph context to form a cohesive response to the original user query.
        """

        return query

    def query_llm(self, query, max_length=400, temperature=0.7):
        """
        Query the LLM and return a formatted response.
        """
        response = self.llm(query, max_length=max_length, truncation=True,
                            temperature=temperature, do_sample=True)
        return response[0]["generated_text"]


# Example Usage
if __name__ == "__main__":
    # Initialize LLM handler
    llm_handler = LLMHandler()

    # Load embeddings and use the first vector as a test query
    embeddings = np.load("embeddings_output/text_embeddings.npy")
    #example_query_vector = np.expand_dims(embeddings[0], axis=0)    
    example_query_text = "Who is Alan Turing?"
    example_query_vector = llm_handler.vector_search_handler.embed_query(example_query_text)

    # Build a vector index and load
    llm_handler.vector_search_handler.build_index(embeddings)
    llm_handler.vector_search_handler.load_index()

    # Perform vector search on query vector and embeddings dataset
    vector_search_results = llm_handler.get_vector_search_results(
        example_query_vector, top_k=5)
    indices = vector_search_results["indices"]
    print(f"VS Indices Returned: {indices}")
    
    # Get texts based on VS indices
    vector_search_texts = llm_handler.get_documents_by_indices(indices)
    
    # Mock knowledge graph output
    kg_output = "Alan Turing developed the idea of the turing machine."

    # Format query and get LLM response
    query = llm_handler.format_query(example_query_text, vector_search_texts, kg_output)
    print("Query to LLM:\n", query)

    response = llm_handler.query_llm(query)
    print("LLM Response:\n", response)
