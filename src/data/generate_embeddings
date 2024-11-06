import pandas as pd
import torch
from transformers import BertTokenizer, BertModel
import numpy as np
import os

# Load Wikipedia data
data_path = 'src/data/simpleWikiData.parquet'
data = pd.read_parquet(data_path)

# Initialize BERT model and tokenizer
model_name = "bert-base-uncased"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name).to('cuda' if torch.cuda.is_available() else 'cpu')
model.eval()  # Set to evaluation mode

# Function to generate embeddings for a given text
def generate_embedding(text):
   inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
   inputs = {key: value.to('cuda') for key, value in inputs.items()} if torch.cuda.is_available() else inputs
   with torch.no_grad():
       outputs = model(**inputs)

   # Use the mean of the last hidden states as the sentence embedding
   return outputs.last_hidden_state.mean(dim=1).cpu().numpy()

# Generate embeddings and store in list
embeddings = []
text_data = data['text']  # Replace 'text' with the actual column name in simpleWikiData.parquet

for text in text_data:
   embedding = generate_embedding(text)
   embeddings.append(embedding)

# Convert list of embeddings to numpy array
embeddings_array = np.vstack(embeddings)

# Save embeddings to file
output_path = 'src/data/wikipedia_embeddings.npy'
np.save(output_path, embeddings_array)
print(f"Embeddings saved to {output_path}")