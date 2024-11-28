import os

#########################################################
### TODO: MAKE MORE ROBUST CONFIG FILE FOR FILE PATHS ###
#########################################################

# Base directory for data processing
BASE_DATA_DIR = "./backend/app/data_processing"

# Subdirectories for specific handlers
EMBEDDINGS_DATA_DIR = os.path.join(BASE_DATA_DIR, "embeddings_data")
VECTOR_SEARCH_DATA_DIR = os.path.join(BASE_DATA_DIR, "vector_search_data")
LLM_DATA_DIR = os.path.join(BASE_DATA_DIR, "llm_data")

# Common file paths
WIKI_DATA_FILE = os.path.join(BASE_DATA_DIR, "simpleWikiData.parquet")
CLEAN_WIKI_DATA_FILE = os.path.join(EMBEDDINGS_DATA_DIR, "clean_wiki_data.parquet")
EMBEDDINGS_FILE = os.path.join(EMBEDDINGS_DATA_DIR, "text_embeddings.npy")
FAISS_INDEX_FILE = os.path.join(VECTOR_SEARCH_DATA_DIR, "index.faiss")
