import spacy
import warnings
from backend.app.main import app
from fastapi.testclient import TestClient

warnings.filterwarnings("ignore", category=DeprecationWarning)
nlp = spacy.load("en_core_web_sm")
client = TestClient(app)


def test_process_query_basic():
    response = client.post("/nlp/process_query",
                           json={"query": "What is the capital of France?"})
    assert response.status_code == 200
    data = response.json()

    # Check if response contains expected fields
    assert "tokens" in data
    assert "entities" in data
    assert "is_harmful" in data
    assert "sparql_query" in data

    # Validate tokens
    assert "What" in data["tokens"]
    assert "capital" in data["tokens"]
    assert "France" in data["tokens"]

    # Validate entities
    assert len(data["entities"]) > 0  # At least one entity, like 'France'

    # Validate harmful intent detection
    assert data["is_harmful"] is False

    # Validate SPARQL query generation
    assert data["sparql_query"] == 'SELECT ?abstract WHERE { ?subject rdfs:label "France"@en . ?subject dbo:abstract ?abstract . }'


def test_process_query_harmful_intent():
    response = client.post("/nlp/process_query",
                           json={"query": "I want to kill someone."})
    assert response.status_code == 200
    data = response.json()

    # Check harmful intent detection
    assert data["is_harmful"] is True


def test_process_query_no_entities():
    response = client.post("/nlp/process_query",
                           json={"query": "Tell me about the weather."})
    assert response.status_code == 200
    data = response.json()

    # Validate that no entities are extracted
    assert len(data["entities"]) == 0


def test_process_query_multiple_entities():
    response = client.post(
        "/nlp/process_query", json={"query": "Tell me about the Eiffel Tower in Paris."})
    assert response.status_code == 200
    data = response.json()

    # Check that both "Eiffel Tower" and "Paris" are recognized as entities
    assert len(data["entities"]) > 1
    assert any(ent["text"] == "the Eiffel Tower" for ent in data["entities"])
    assert any(ent["text"] == "Paris" for ent in data["entities"])
