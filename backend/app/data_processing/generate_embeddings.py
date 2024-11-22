import pandas as pd
import numpy as np
from transformers import BertTokenizer, BertModel
import torch
import os

# Configuration
DATA_FILE = "simpleWikiData.parquet"  # Replace with the path to your dataset
TEXT_COLUMN = "text"  # Replace with the name of the column containing text
OUTPUT_DIR = "embeddings_output"  # Directory to save embeddings
BATCH_SIZE = 16  # Adjust based on your GPU/CPU memory


# Step 1: Load Dataset
def load_dataset(file_path):
    print("Loading dataset...")
    data = pd.read_parquet(file_path)
    return data


# Step 2: Prepare BERT Model and Tokenizer
def load_bert_model():
    print("Loading BERT model...")
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    model = BertModel.from_pretrained("bert-base-uncased")
    model.eval()
    if torch.cuda.is_available():
        model = model.cuda()
    return tokenizer, model


# Step 3: Generate Embeddings
def generate_embeddings(texts, tokenizer, model, batch_size=16):
    embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        inputs = tokenizer(batch, padding=True, truncation=True, return_tensors="pt", max_length=512)
        if torch.cuda.is_available():
            inputs = {key: val.cuda() for key, val in inputs.items()}
        with torch.no_grad():
            outputs = model(**inputs)
            # Use the CLS token representation
            batch_embeddings = outputs.last_hidden_state[:, 0, :].cpu().numpy()
            embeddings.append(batch_embeddings)
        print(f"Processed {i + len(batch)}/{len(texts)} texts")
    return np.vstack(embeddings)


# Step 4: Save Embeddings
def save_embeddings(embeddings, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "text_embeddings.npy")
    np.save(output_path, embeddings)
    print(f"Embeddings saved to {output_path}")


# Main Function
def main():
    # Load dataset
    data = load_dataset(DATA_FILE)

    # Filter out rows with empty text
    texts = data[TEXT_COLUMN].dropna().tolist()

    # **Modify this line to use only a subset for testing**
    subset_size = 100  # Number of rows to use for testing
    texts = texts[:subset_size]  # Select only the first `subset_size` rows

    print(f"Loaded {len(texts)} rows of text for embedding.")

    # Load BERT model
    tokenizer, model = load_bert_model()

    # Generate embeddings
    embeddings = generate_embeddings(texts, tokenizer, model, batch_size=BATCH_SIZE)

    # Save embeddings
    save_embeddings(embeddings, OUTPUT_DIR)


if __name__ == "__main__":
    main()
