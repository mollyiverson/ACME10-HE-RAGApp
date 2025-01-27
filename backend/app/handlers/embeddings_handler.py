import os
import pandas as pd
import numpy as np
import torch
from transformers import BertTokenizer, BertModel
from backend.app.data_processing.pdf_data_extractor import extract_text_from_pdfs, texts_to_dataframe, save_dataframe_to_parquet

##############################################################
### TODO: USE IMPORTS WHEN CONFIG FILE IS CORRECTLY SET UP ###
##############################################################
# from backend.app.config import EMBEDDINGS_DATA_DIR, WIKI_DATA_FILE, CLEAN_WIKI_DATA_FILE

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
PDF_PARQUET_FILE = os.path.join(BASE_DATA_DIR, "pdf_data.parquet")
CLEAN_WIKI_DATA_FILE = os.path.join(EMBEDDINGS_DATA_DIR, "clean_wiki_data.parquet")
EMBEDDINGS_FILE = os.path.join(EMBEDDINGS_DATA_DIR, "text_embeddings.npy")
FAISS_INDEX_FILE = os.path.join(VECTOR_SEARCH_DATA_DIR, "index.faiss")

TEXT_COLUMN = "text"  # Replace with the name of the column containing text
BATCH_SIZE = 16  # Adjust based on your GPU/CPU memory
SUBSET_SIZE = 100  # Number of rows to use for embeddings

# Step 1: Load Dataset
def load_dataset(dataset_path):
    print("Loading dataset...")
    if not os.path.exists(dataset_path):
        print(f"Error: {dataset_path} does not exist.")
    else:
        print(f"File found: {dataset_path}")
        data = pd.read_parquet(dataset_path)
        print(f"Loaded {len(data)} rows of text.")
        return data

# Step 2: Clean the dataset
def clean_dataset(data):
    print("Cleaning dataset...")
    cleaned_data = data[[TEXT_COLUMN]].dropna()  # Retain the DataFrame structure
    print(f"Cleaned data: {len(cleaned_data)} rows remaining.")
    return cleaned_data

# Step 3: Save the cleaned dataset
def save_dataset(data):
    os.makedirs(EMBEDDINGS_DATA_DIR, exist_ok=True)
    data.to_parquet(CLEAN_WIKI_DATA_FILE)
    print(f"Cleaned dataset saved to: {CLEAN_WIKI_DATA_FILE}")

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
def generate_embeddings(texts, tokenizer, model, batch_size=BATCH_SIZE):
    embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        inputs = tokenizer(batch, padding=True, truncation=True, return_tensors="pt", max_length=512)
        if torch.cuda.is_available():
            inputs = {key: val.cuda() for key, val in inputs.items()}
        with torch.no_grad():
            outputs = model(**inputs)
            batch_embeddings = outputs.last_hidden_state[:, 0, :].cpu().numpy()  # Use the CLS token representation
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
    # Convert PDFs to Parquet format
    pdf_dir = 'backend/app/data_processing/embeddings_data/embeddings_pdf'
    output_parquet_path = PDF_PARQUET_FILE
    texts = extract_text_from_pdfs(pdf_dir)
    df = texts_to_dataframe(texts)
    save_dataframe_to_parquet(df, output_parquet_path)

    # Load datasets
    wiki_data = load_dataset(WIKI_DATA_FILE)
    pdf_data = load_dataset(PDF_PARQUET_FILE)

    # Combine datasets
    concat_data = pd.concat([wiki_data, pdf_data], ignore_index=True)

    # Clean dataset
    clean_data = clean_dataset(concat_data)

    # Save the cleaned dataset
    save_dataset(clean_data)

    # Select a subset for testing
    texts = clean_data[TEXT_COLUMN].iloc[:SUBSET_SIZE].tolist()
    print(f"Loaded {len(texts)} rows of text for embedding.")

    # Load BERT model
    tokenizer, model = load_bert_model()

    # Generate embeddings
    embeddings = generate_embeddings(texts, tokenizer, model)

    # Save embeddings
    save_embeddings(embeddings, EMBEDDINGS_DATA_DIR)

if __name__ == "__main__":
    main()