from transformers import BertTokenizer, BertModel
import torch
import faiss
import numpy as np
import pandas as pd
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
        """Build a FAISS index with cosine similarity (as opposed to L2 distance)."""
        # Normalize embeddings
        embeddings_normalized = embeddings / np.linalg.norm(embeddings, axis=1)[:, np.newaxis]
        
        dimension = embeddings.shape[1]
        # Use Inner Product index for cosine similarity
        self.index = faiss.IndexFlatIP(dimension)  
        self.index.add(embeddings_normalized)
        print(f"Index built with {self.index.ntotal} vectors.")


    def load_index(self):
        #######################################################################
        ### TODO: Refactor to separate NLP handler code and the router code ###
        #######################################################################
        """Load an existing FAISS index."""
        if not os.path.exists(self.index_path):
            raise FileNotFoundError(f"Index file not found: {self.index_path}")
        self.index = faiss.read_index(self.index_path)
    
    def embed_query(self, query):
        """
        Generate an embedding for the query using BERT with mean pooling.
        """
        inputs = self.tokenizer(query, return_tensors="pt", padding=True, truncation=True, max_length=512)
        if torch.cuda.is_available():
            inputs = {key: val.cuda() for key, val in inputs.items()}
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            # Mean pooling
            attention_mask = inputs['attention_mask']
            token_embeddings = outputs.last_hidden_state
            
            # Create mask of which tokens are padding
            input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
            
            # Sum embeddings while respecting the attention mask
            sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
            
            # Count of non-padding tokens
            sum_mask = input_mask_expanded.sum(1)
            
            # Avoid division by zero
            sum_mask = torch.clamp(sum_mask, min=1e-9)
            
            # Calculate mean
            query_embedding = sum_embeddings / sum_mask
            query_embedding = query_embedding.cpu().numpy()
        
        return query_embedding

    def search(self, query_vector, top_k=5):
        """Search the FAISS index with normalized query vector."""
        if self.index is None:
            raise ValueError("Index is not loaded. Build or load an index first.")
        
        # Normalize query vector
        query_vector_normalized = query_vector / np.linalg.norm(query_vector, axis=1)[:, np.newaxis]
        
        # Use inner product (which returns similarities, not distances)
        similarities, indices = self.index.search(query_vector_normalized, top_k)

        print("Index-Similarity Scores:")
        for i, s in zip(indices[0], similarities[0]):
            print(f"Index {i}: {s}")
        print("\n")

        return similarities[0], indices[0]
    
    def get_search_results(self, indices, dataset_path="embeddings_output/clean_wiki_data.parquet"):
        """Get the corresponding texts of the top VS results."""
        # Load the dataset
        original_data = pd.read_parquet(dataset_path)
        
        # Extract the texts using the provided indices
        selected_texts = original_data.iloc[indices]["text"].tolist()
        
        # Print the relevant results
        print("Relevant results from embeddings:")
        for i, text in zip(indices, selected_texts):
            print(f"Index {i}: {text}\n")
        
        return selected_texts 


# Example Usage
if __name__ == "__main__":
    handler = VectorSearchHandler(embedding_path="embeddings_output/text_embeddings.npy")

    # Load embeddings and build index
    embeddings = handler.load_embeddings()
    handler.build_index(embeddings)

    # Search example (query vector must have the same dimension as embeddings)
    example_query_text = "Who is Alan Turing?"
    example_query_vector = handler.embed_query(example_query_text)
    similarities, indices = handler.search(example_query_vector)
    
    # Get search results
    handler.get_search_results(indices)
