import pandas as pd
import numpy as np
from transformers import BertTokenizer, BertModel
from sentence_transformers import SentenceTransformer
import faiss
import os
##############################
### TODO: FIX IMPORT ERROR ###
##############################
#from backend.app.config import EMBEDDINGS_FILE, FAISS_INDEX_FILE

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

class VectorSearchHandler:
    def __init__(self, embedding_path=EMBEDDINGS_FILE, index_path=FAISS_INDEX_FILE):
        self.embedding_path = embedding_path
        self.index_path = index_path
        self.index = None

        # Initialize model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def load_embeddings(self):
        """Load embeddings from the specified path."""
        if not os.path.exists(self.embedding_path):
            raise FileNotFoundError(f"Embedding file not found: {self.embedding_path}")
        return np.load(self.embedding_path)

    def build_index(self, embeddings):
        """Build a FAISS index with cosine similarity."""
        embeddings_normalized = embeddings / np.linalg.norm(embeddings, axis=1)[:, np.newaxis]
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)  
        self.index.add(embeddings_normalized)
        print(f"Index built with {self.index.ntotal} vectors.")

        os.makedirs(VECTOR_SEARCH_DATA_DIR, exist_ok=True)
        faiss.write_index(self.index, self.index_path)

    def load_index(self):
        """Load an existing FAISS index."""
        if not os.path.exists(self.index_path):
            raise FileNotFoundError(f"Index file not found: {self.index_path}")
        self.index = faiss.read_index(self.index_path)

    def embed_query(self, query):
        """Generate an embedding for the query."""
        query_embedding = self.model.encode(query, convert_to_numpy=True)
        
        return query_embedding

    def search(self, query_vector, top_k=10, similarity_threshold=0.3):
        """Search the FAISS index with normalized query vector."""
        if self.index is None:
            raise ValueError("Index is not loaded. Build or load an index first.")

        query_vector_normalized = query_vector / np.linalg.norm(query_vector)
        query_vector_normalized = query_vector_normalized.reshape(1, -1)  # Reshape to 2D (1, d)

        similarities, indices = self.index.search(query_vector_normalized, top_k)

        # Filter results below the threshold
        filtered_results = [
            (similarity, index)
            for similarity, index in zip(similarities[0], indices[0])
            if similarity >= similarity_threshold
        ]

        if not filtered_results:
            return [], []  # No results above threshold

        filtered_similarities, filtered_indices = zip(*filtered_results)
    
        return list(filtered_similarities), list(filtered_indices)

    def get_search_results(self, indices, dataset_path=CLEAN_WIKI_DATA_FILE):
        """Get the corresponding texts of the top results."""
        original_data = pd.read_parquet(dataset_path)
        return original_data.iloc[indices]["text"].tolist()

# Example Usage
if __name__ == "__main__":
    handler = VectorSearchHandler()

    embeddings = handler.load_embeddings()
    handler.build_index(embeddings)

    example_query_text = "How many people in Guatemala are Native American?"
    example_query_vector = handler.embed_query(example_query_text)
    similarities, indices = handler.search(example_query_vector)

    vector_search_texts = handler.get_search_results(indices)
    print("Search Results:\n", vector_search_texts)
