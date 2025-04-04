import pytest
import numpy as np
from backend.app.handlers.llm_handler import LLMHandler


@pytest.fixture
def llm_handler():
    """Fixture to initialize the LLM handler."""
    return LLMHandler(embedding_path="embeddings_output/text_embeddings.npy")


@pytest.fixture
def mock_vector_search_results():
    """Fixture for mocked vector search results."""
    return {"indices": [0, 1, 2], "distances": [0.0, 12.3, 45.6]}


@pytest.fixture
def mock_kg_output():
    """Fixture for mocked knowledge graph output."""
    return "Connections between NLP and Knowledge Graphs."


def test_query_llm_max_length(llm_handler, mock_vector_search_results, mock_kg_output):
    original_query = "What is the relationship between NLP and Knowledge Graphs?"
    query = llm_handler.format_query(original_query, mock_vector_search_results, mock_kg_output)
    response = llm_handler.query_llm(query)
    
    assert isinstance(response, str)
    assert len(response.split()) <= 200, "LLM response exceeds max length constraint"

