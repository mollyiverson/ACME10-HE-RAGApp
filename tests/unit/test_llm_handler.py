import pytest
import numpy as np
from backend.app.llm_handler import LLMHandler


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


def test_format_query(llm_handler, mock_vector_search_results, mock_kg_output):
    query = llm_handler.format_query(mock_vector_search_results, mock_kg_output)
    assert "Vector Search Results" in query
    assert "Knowledge Graph Results" in query


def test_query_llm(llm_handler, mock_vector_search_results, mock_kg_output):
    query = llm_handler.format_query(mock_vector_search_results, mock_kg_output)
    response = llm_handler.query_llm(query, max_length=50)
    assert isinstance(response, str)
    assert len(response) > 0
