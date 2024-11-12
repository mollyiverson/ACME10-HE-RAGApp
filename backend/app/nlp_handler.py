import spacy
from fastapi import APIRouter
from pydantic import BaseModel
from spacy.tokens import Span

router = APIRouter()
nlp = spacy.load("en_core_web_sm")


class Query(BaseModel):
    query: str


def detect_harmful_intent(doc):
    harmful_keywords = ["kill", "attack", "destroy", "harm"]
    for token in doc:
        if token.lemma_.lower() in harmful_keywords:
            return True
    return False


def extract_entities(doc):
    return [{"text": ent.text, "label": ent.label_} for ent in doc.ents]


def tokenize_text(doc):
    return [token.text for token in doc]


def generate_sparql_query(entities):
    if entities:
        entity = entities[0]["text"]
        return f"SELECT ?abstract WHERE {{ ?subject rdfs:label \"{entity}\"@en . ?subject dbo:abstract ?abstract . }}"
    return None


@router.post("/process_query")
def process_query(query: Query):
    doc = nlp(query.query)
    tokens = tokenize_text(doc)
    entities = extract_entities(doc)
    is_harmful = detect_harmful_intent(doc)

    sparql_query = generate_sparql_query(entities)

    return {
        "tokens": tokens,
        "entities": entities,
        "is_harmful": is_harmful,
        "sparql_query": sparql_query
    }
