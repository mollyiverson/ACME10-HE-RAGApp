import unittest
import numpy as np
from vector_search_handler import VectorSearchHandler

class TestVectorSearchHandler(unittest.TestCase):
    def setUp(self):
        # Create a small set of dummy embeddings
        self.embeddings = np.random.random((10, 128)).astype(np.float32)  # 10 vectors of 128 dimensions
        self.handler = VectorSearchHandler(embedding_path="embeddings_output/text_embeddings.npy")

        # Save embeddings to test file
        np.save(self.handler.embedding_path, self.embeddings)

    def tearDown(self):
        # Cleanup test files
        import os
        if os.path.exists(self.handler.embedding_path):
            os.remove(self.handler.embedding_path)
        if os.path.exists(self.handler.index_path):
            os.remove(self.handler.index_path)

    def test_load_embeddings(self):
        loaded_embeddings = self.handler.load_embeddings()
        self.assertTrue(np.array_equal(loaded_embeddings, self.embeddings))

    def test_build_index(self):
        self.handler.build_index(self.embeddings)
        self.assertEqual(self.handler.index.ntotal, len(self.embeddings))

    def test_search(self):
        self.handler.build_index(self.embeddings)
        query = np.expand_dims(self.embeddings[0], axis=0)
        distances, indices = self.handler.search(query, top_k=3)
        self.assertEqual(len(indices[0]), 3)  # Ensure we get 3 results

if __name__ == "__main__":
    unittest.main()
