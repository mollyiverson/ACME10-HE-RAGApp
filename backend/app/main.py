from fastapi import FastAPI
from .nlp_handler import router as nlp_router
from .dbpedia_query import router as dbpedia_router

app = FastAPI()

app.include_router(nlp_router, prefix="/nlp")
app.include_router(dbpedia_router, prefix="/dbpedia")

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}