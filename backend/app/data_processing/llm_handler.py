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
        Perform vector search and retrieve top-k results.
        """
        distances, indices = self.vector_search_handler.search(
            query_vector, top_k=top_k)
        return {"distances": distances, "indices": indices}

    def format_query(self, vector_search_results, kg_output):
        """
        Combine VS and KG outputs into a single natural-language query.
        """
        query = f"""
        Based on the following context:
        Vector Search Results: {vector_search_results}
        Knowledge Graph Results: {kg_output}

        Provide a detailed, natural-language response.
        """
        return query

    def query_llm(self, query, max_length=200, temperature=0.7):
        """
        Query the LLM and return a formatted response.
        """
        response = self.llm(query, max_length=max_length,
                            temperature=temperature, do_sample=True)
        return response[0]["generated_text"]


# Example Usage
if __name__ == "__main__":
    # Initialize LLM handler
    llm_handler = LLMHandler()

    # Load embeddings and use the first vector as a test query
    embeddings = np.load("embeddings_output/text_embeddings.npy")
    example_query_vector = np.expand_dims(embeddings[0], axis=0)

    # Perform vector search
    vector_search_results = llm_handler.get_vector_search_results(
        example_query_vector, top_k=5)

    # Mock knowledge graph output
    kg_output = "Connections between natural language processing and AI ethics."

    # Format query and get LLM response
    query = llm_handler.format_query(vector_search_results, kg_output)
    print("Query to LLM:\n", query)

    response = llm_handler.query_llm(query)
    print("LLM Response:\n", response)
