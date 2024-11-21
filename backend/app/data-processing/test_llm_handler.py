import unittest
import numpy as np
from llm_handler import LLMHandler

class TestLLMHandler(unittest.TestCase):
    def setUp(self):
        # Initialize the LLM handler
        self.llm_handler = LLMHandler(embedding_path="embeddings_output/text_embeddings.npy")

        # Load embeddings and mock vector search results
        self.embeddings = np.load("embeddings_output/text_embeddings.npy")
        self.query_vector = np.expand_dims(self.embeddings[0], axis=0)
        self.kg_output = "Sample knowledge graph output."

    def test_vector_search_results(self):
        results = self.llm_handler.get_vector_search_results(self.query_vector, top_k=3)
        self.assertIn("indices", results)
        self.assertIn("distances", results)

    def test_format_query(self):
        vector_search_results = {"indices": [0, 1, 2], "distances": [0.0, 12.3, 45.6]}
        query = self.llm_handler.format_query(vector_search_results, self.kg_output)
        self.assertIn("Vector Search Results", query)
        self.assertIn("Knowledge Graph Results", query)

    def test_query_llm(self):
        vector_search_results = {"indices": [0, 1, 2], "distances": [0.0, 12.3, 45.6]}
        query = self.llm_handler.format_query(vector_search_results, self.kg_output)
        response = self.llm_handler.query_llm(query, max_length=50)
        self.assertTrue(isinstance(response, str))
        self.assertGreater(len(response), 0)

if __name__ == "__main__":
    unittest.main()
