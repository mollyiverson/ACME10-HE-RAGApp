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
def load_dataset(dataset_path):
    print("Loading dataset...")
    data = pd.read_parquet(dataset_path)
    print(f"Loaded {len(data)} rows of text.")

    return data

# Step 2: Clean the dataset
def clean_dataset(data):
    print("Cleaning dataset...")
    # Filter out rows where the TEXT_COLUMN is NaN
    cleaned_data = data[[TEXT_COLUMN]].dropna()  # Retain the DataFrame structure
    print(f"Cleaned data: {len(cleaned_data)} rows remaining.")

    return cleaned_data

# Step 3: Save the cleaned dataset
def save_dataset(data, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    # Save cleaned data as parquet
    texts_path = os.path.join(output_dir, "clean_wiki_data.parquet")
    data.to_parquet(texts_path)

    print(f"Cleaned dataset saved to: {texts_path}")

# Step 4: Prepare BERT Model and Tokenizer
def load_bert_model():
    print("Loading BERT model...")
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    model = BertModel.from_pretrained("bert-base-uncased")
    model.eval()
    if torch.cuda.is_available():
        model = model.cuda()
    return tokenizer, model


# Step 5: Generate Embeddings
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


# Step 6: Save Embeddings
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
    clean_data = clean_dataset(data)

    # Save the cleaned dataset
    save_dataset(clean_data, OUTPUT_DIR)

    # **Modify this line to use only a subset for testing**
    subset_size = 100  # Number of rows to use for testing
    texts = clean_data[TEXT_COLUMN].iloc[:subset_size].tolist()  # Extract a subset of text as a list

    print(f"Loaded {len(texts)} rows of text for embedding.")

    # Load BERT model
    tokenizer, model = load_bert_model()

    # Generate embeddings
    embeddings = generate_embeddings(texts, tokenizer, model, batch_size=BATCH_SIZE)

    # Save embeddings
    save_embeddings(embeddings, OUTPUT_DIR)


if __name__ == "__main__":
    main()
