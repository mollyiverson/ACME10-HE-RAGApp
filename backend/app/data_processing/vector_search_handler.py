from transformers import BertTokenizer, BertModel
import torch
import faiss
import numpy as np
import os

class VectorSearchHandler:
    def __init__(self, embedding_path, index_path="index.faiss"):
        self.embedding_path = embedding_path
        self.index_path = index_path
        self.index = None

        # Initialize BERT tokenizer and model
        self.tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
        self.model = BertModel.from_pretrained("bert-base-uncased")
        self.model.eval()
        if torch.cuda.is_available():
            self.model = self.model.cuda()

    def load_embeddings(self):
        """Load embeddings from the specified path."""
        if not os.path.exists(self.embedding_path):
            raise FileNotFoundError(f"Embedding file not found: {self.embedding_path}")
        return np.load(self.embedding_path)

    def build_index(self, embeddings):
        """Build a FAISS index from the embeddings."""
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)  # Use L2 (Euclidean) distance
        self.index.add(embeddings)
        print(f"Index built with {self.index.ntotal} vectors.")

        # Optionally save the index
        faiss.write_index(self.index, self.index_path)

    def load_index(self):
        """Load an existing FAISS index."""
        if not os.path.exists(self.index_path):
            raise FileNotFoundError(f"Index file not found: {self.index_path}")
        self.index = faiss.read_index(self.index_path)
    
    def embed_query(self, query):
        """
        Generate an embedding for the query using BERT.
        """
        inputs = self.tokenizer(query, return_tensors="pt", padding=True, truncation=True, max_length=512)
        if torch.cuda.is_available():
            inputs = {key: val.cuda() for key, val in inputs.items()}
        with torch.no_grad():
            outputs = self.model(**inputs)
            # Use the CLS token representation for the query embedding
            query_embedding = outputs.last_hidden_state[:, 0, :].cpu().numpy()

        return query_embedding


    def search(self, query_vector, top_k=5):
        """Search the FAISS index for the most similar vectors."""
        if self.index is None:
            raise ValueError("Index is not loaded. Build or load an index first.")
        distances, indices = self.index.search(query_vector, top_k)
        return distances, indices

# Example Usage
if __name__ == "__main__":
    handler = VectorSearchHandler(embedding_path="embeddings_output/text_embeddings.npy")

    # Load embeddings and build index
    embeddings = handler.load_embeddings()
    handler.build_index(embeddings)

    # Search example (query vector must have the same dimension as embeddings)
    example_query = np.expand_dims(embeddings[0], axis=0)  # Use the first vector as a query
    distances, indices = handler.search(example_query)
    print(f"Top results: {indices}, Distances: {distances}")
