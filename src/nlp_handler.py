from fastapi import FastAPI
import spacy

app = FastAPI()

nlp = spacy.load("en_core_web_sm")

def detect_harmful_intent(doc):
    harmful_keywords = ["kill", "attack", "destroy", "harm"]
    for token in doc:
        if token.lemma_.lower() in harmful_keywords:
            return True
    return False

@app.post("/process_query")
def process_query(query: str):
    doc = nlp(query)
    tokens = [token.text for token in doc]
    entities = [ent.label_ for ent in doc.ents]
    is_harmful = detect_harmful_intent(doc)
    
    return {
        "tokens": tokens,
        "entities": entities,
        "is_harmful": is_harmful
    }