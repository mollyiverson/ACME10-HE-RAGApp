import logging
import urllib.parse
from fastapi import APIRouter
from pydantic import BaseModel
from SPARQLWrapper import SPARQLWrapper, JSON

router = APIRouter()

class Query(BaseModel):
    query: str

@router.post("/querykg")
def query_dbpedia(query: Query):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)

    logging.info("SPARQL query being sent: %s", query.query)

    try:
        sparql.setQuery(query.query)
        results = sparql.query().convert()
        return results
    except Exception as e:
        logging.error("Error executing SPARQL query: %s", e)
        raise

"""Helper function to format DBpedia resources by encoding special characters."""
def encode_resource(name: str) -> str:
    return urllib.parse.quote(name.replace(" ", "_"))
