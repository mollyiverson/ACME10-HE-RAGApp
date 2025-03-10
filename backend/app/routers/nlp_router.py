import spacy
from fastapi import APIRouter
from backend.app.models.basic_query import Query
from backend.app.handlers.llm_handler import LLMHandler

router = APIRouter()
nlp = spacy.load("en_core_web_sm")

# Initialize LLM handler
llm_handler = LLMHandler()

#######################################################################
### TODO: Refactor to separate NLP handler code and the router code ###
#######################################################################

def detect_harmful_intent(doc):
    '''
    Detects harmful intent within a processed document by checking for keywords associated with harmful actions.
    :param doc: <spacy.tokens.Doc> Processed text document.
    :return: <bool> True if harmful intent keywords are found; False otherwise.
    '''
    harmful_keywords = ["kill", "attack", "destroy", "harm"]
    for token in doc:
        if token.lemma_.lower() in harmful_keywords:
            return True
    return False


def extract_entities(doc):
    '''
    Extracts named entities from the processed document for further use.
    :param doc: <spacy.tokens.Doc> Processed text document.
    :return: <list of dict> List of entities with 'text' and 'label' for each.
    '''
    return [{"text": ent.text, "label": ent.label_} for ent in doc.ents]


def tokenize_text(doc):
    '''
    Tokenizes the document text into individual words and punctuation marks.
    :param doc: <spacy.tokens.Doc> Processed text document.
    :return: <list of str> List of token strings.
    '''

    return [token.text for token in doc]


def generate_sparql_query(entities):
    '''
    Generates a SPARQL query to retrieve abstract information for the first identified entity in the document.
    :param entities: <list of dict> List of extracted entities with 'text' and 'label'.
    :return: <str or None> SPARQL query string if entities exist, otherwise None.
    '''

    if entities:
        entity = entities[0]["text"]
        return f"""
        SELECT ?abstract WHERE {{
            ?subject rdfs:label "{entity}"@en .
            ?subject dbo:abstract ?abstract .
            FILTER (lang(?abstract) = 'en')
        }}
        """
    return None


@router.post("/process_query")
def process_query(query: Query):
    '''
    Processes a user query by performing various NLP tasks including tokenization, entity extraction, 
    harmful intent detection, and optionally generating a SPARQL query if entities are found.
    :param query: <Query> Pydantic model containing the user's input text as 'query'.
    :return: <dict> Dictionary with tokens, entities, harmful intent status, and a SPARQL query if applicable.
    '''

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

@router.post("/llm_response")
def llm_respond(query: Query, vector_search_results = [], kg_results = ""):
    """
    Processes an LLM response for the given query and supporting data.
    
    :param query: <Query> Pydantic model containing the user's input text as 'query'.
    :param vector_search_results: <string> Results from a vector search.
    :param kg_results: <string> Results from a knowledge graph query.
    :return: <string> LLM response or an error message.
    """
    try:
        # Format query and get LLM response
        formatted_query = llm_handler.format_query(query, vector_search_results, kg_results)
        response = llm_handler.query_llm(formatted_query)

        return { "response": response }

    except ValueError as ve:
        # Handle specific value-related errors
        return {"error": "Value error encountered", "details": str(ve)}, 400

    except AttributeError as ae:
        # Handle attribute-related errors
        return {"error": "Attribute error encountered", "details": str(ae)}, 400

    except Exception as e:
        # Catch any other exceptions and return a generic error response
        return {"error": "An unexpected error occurred", "details": str(e)}, 500
