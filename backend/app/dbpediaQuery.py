from fastapi import APIRouter, FastAPI
from SPARQLWrapper import SPARQLWrapper, JSON

router = APIRouter()


def query_dbpedia(query: str):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results


@router.get("/querykg")
def read_query(subject: str, predicate: str):
    query = f"""
    SELECT ?object WHERE {{
        dbr:{subject} dbo:{predicate} ?object
    }}
    """
    results = query_dbpedia(query)
    return results
