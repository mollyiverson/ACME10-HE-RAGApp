import logging
import urllib.parse
from fastapi import APIRouter
from SPARQLWrapper import SPARQLWrapper, JSON
from app.models.basic_query import Query

router = APIRouter()

@router.post("/querykg")
def query_dbpedia(query: Query):
    '''
    Executes a SPARQL query against the DBpedia knowledge graph.
    :param query: <Query> The SPARQL query to execute.
    :return: <dict> The query results in JSON format.
    '''
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
