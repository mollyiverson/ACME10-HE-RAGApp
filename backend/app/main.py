from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .nlp_handler import router as nlp_router
from .dbpedia_query_handler import router as dbpedia_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:3000",
        "http://127.0.0.1",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(nlp_router, prefix="/nlp")
app.include_router(dbpedia_router, prefix="/dbpedia")


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}
