# Sprint 2 Report (10/6/2024 - 11/5/2024)

[Sprint 2 Video Link](https://www.youtube.com/watch?v=UCjLWCaOBvQ)

## What's New (User Facing)
* Developed a basic chat interface for the RAG application in Figma, with user input and response capabilities.
* Integrated BERT embeddings for a subset of the Wikipedia dataset, essential for vector search functionality.
* Set up initial DBpedia querying for knowledge graph integration.
* Wrote some query processing code using NLP libraries.
* Created the foundational system architecture documentation, including database optimization strategies.

## Work Summary (Developer Facing)
In this sprint, our team made significant progress on foundational components for the RAG application, focusing on embedding generation, frontend prototyping, and knowledge graph querying. We researched and implemented BERT embeddings, setting up our application for vector search with FAISS. The frontend was designed with a minimalist chat-style interface, which received positive feedback from the client. Additionally, we integrated initial queries with DBpedia, allowing us to retrieve semantic information. Major challenges included the computational demands of embedding large datasets, which highlighted the need for GPU support in future sprints. Our team overcame these barriers through collaboration, dividing responsibilities effectively across frontend, backend, and database optimizations.

## Unfinished Work
* Generating embeddings for the full Wikipedia dataset. Due to computational limitations, we processed only a subset and will scale up with GPU support in the next sprint.

## Completed Issues/User Stories
Here are links to the issues that we completed in this sprint:

* [Plan semester project milestones](https://github.com/mollyiverson/ACME10-HE-RAGApp/issues/36)
* [Extract from Wikipedia dataset using Python](https://github.com/mollyiverson/ACME10-HE-RAGApp/issues/38)
* [Revise Requirements and Specifications document](https://github.com/mollyiverson/ACME10-HE-RAGApp/issues/39)
* [Running BERT embedding on a sample of Wikipedia data](https://github.com/mollyiverson/ACME10-HE-RAGApp/issues/42)
* [Create basic frontend prototype with React](https://github.com/mollyiverson/ACME10-HE-RAGApp/issues/44)
* [Write User Interface Design report section](https://github.com/mollyiverson/ACME10-HE-RAGApp/issues/45)
* [Write solution approach introduction and system overview report sections](https://github.com/mollyiverson/ACME10-HE-RAGApp/issues/46)
* [Create component diagram](https://github.com/mollyiverson/ACME10-HE-RAGApp/issues/47)
* [Create architecture design and subcomponent decomposition report section](https://github.com/mollyiverson/ACME10-HE-RAGApp/issues/48)
* [Write Data Design and chat loader subcomponent sections](https://github.com/mollyiverson/ACME10-HE-RAGApp/issues/49)
* [Integrate Knowledge Graphs in the RAG pipeline](https://github.com/mollyiverson/ACME10-HE-RAGApp/issues/51)
* [Integrated querying DBpedia](https://github.com/mollyiverson/ACME10-HE-RAGApp/issues/52)
* [Write introduction for Testing and Acceptance plans report (overview, test objectives, scope)](https://github.com/mollyiverson/ACME10-HE-RAGApp/issues/53)
* [Write unit and integration tests section](https://github.com/mollyiverson/ACME10-HE-RAGApp/issues/54)
* [Write testing strategy and environmental requirements section](https://github.com/mollyiverson/ACME10-HE-RAGApp/issues/55)
* [Write System testing section (functional, performance, user acceptance)](https://github.com/mollyiverson/ACME10-HE-RAGApp/issues/56)
* [Create code for natural language processing for the query](https://github.com/mollyiverson/ACME10-HE-RAGApp/issues/57)

## Incomplete Issues/User Stories
Here are links to issues we worked on but did not complete in this sprint:

* [Full Wikipedia Embedding Generation](https://github.com/mollyiverson/ACME10-HE-RAGApp/issues/50) - *We only generated embeddings for a subset of the data. Full-scale processing was delayed due to CPU limitations and will require GPU resources.*

## Code Files for Review
Please review the following code files, which were actively developed during this sprint, for quality:
* [Generate Embeddings - Vector Search](https://github.com/mollyiverson/ACME10-HE-RAGApp/blob/main/src/data/generate_embeddings.py) - Code for generating BERT embeddings on the Wikipedia dataset.
* [Frontend Prototype - Chat Interface](https://github.com/mollyiverson/ACME10-HE-RAGApp/blob/main/rag-app/src/App.tsx) - Basic chat interface for user interaction using React.
* [DBpedia Querying Code](https://github.com/mollyiverson/ACME10-HE-RAGApp/blob/main/src/dbpediaQuery.py) - Code to set up and test querying with DBpedia.
* [Natural language processing code](https://github.com/mollyiverson/ACME10-HE-RAGApp/blob/main/src/nlp_handler.py) - Code to break down the query into entities before vector search and knowledge graph querying.

## Retrospective Summary
Here's what went well:
* Collaborative work distribution allowed us to make progress on key components like embeddings, frontend, and knowledge graph integration.
* Positive client feedback on the frontend prototype, validating our UI approach and design choices.
* Successful integration of initial BERT embeddings and DBpedia queries, establishing core functionality.

Here's what we'd like to improve:
* Embedding generation efficiency: Running BERT on large datasets requires GPU support, so we plan to improve our resource allocation and infrastructure.
* Early testing of components: Testing components earlier in the sprint will allow us to identify integration issues sooner.
* Streamlined documentation: Creating more structured documentation during development could ease collaboration and review.

Here are changes we plan to implement in the next sprint:
* Prioritize GPU support for faster embedding generation and handling larger datasets.
* Begin integration of FAISS indexing to enable vector search with the generated embeddings.
* Set up an LLM to generate responses from data given a query.
* Fully integrate NLP and KG into the pipeline.
* Write unit and integration tests.
* Continue developing the backend to combine vector search results with knowledge graph data for more accurate responses.
