# ACME10-HE-RAGApp

## Project summary

### One-sentence description of the project

We will develop a RAG (Retrieval-Augmented Generation) application for [HackerEarth](https://www.hackerearth.com/) that will utilize vector search, knowledge graphs, and a LLM to answer questions and generate content from a knowledge base of more than 10,000 Wikipedia articles.

### Additional information about the project

- **Client:**
  - [HackerEarth](https://www.hackerearth.com/), based in San Francisco, offers enterprise software for technical hiring. Organizations use their platform to create coding assessments, conduct remote video interviews, and ensure unbiased, AI-powered evaluation of candidates.
- **RAG application:**
  - Retrieval Augmented Generation (RAG) means supplying a Large Language Model (LLM) with the appropriate processed data from an outside knowledge base. We will use Knowledge Graphs and vector search to optimize data retrieval. 
- **Potential Knowledge Graph tools:**
  - DBpedia, YAGO, or other knowledge graphs (KG) of your choice, and use SPARQL to query the KG.
- **Potential vector search tools:**
  - FAISS, Annoy, Pinecone, or other vector search libraries.
- **Potential LLMs:**
  - OpenAI, or free models such as Microsoft Phi, Smaller version of LLaMA, etc.

## Installation

### Prerequisites

- **Git:** Ensure that you have Git installed to clone the repository. You can install Git from [here](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).
- **Python 3.9+:** Required to run the backend services of the RAG application.
- **Node.js:** For running the frontend, you need to have Node.js installed. Get it from [here](https://nodejs.org/en/).
- **SPARQL endpoint:** Install or access an instance for querying knowledge graphs.
- **Vector Search Libraries:** Install FAISS or another vector search library (for example, `pip install faiss`).
- **LLM API Key:** If you are using an external LLM (e.g., OpenAI), ensure you have the API key set up in your environment.

### Add-ons

- **React (Frontend):** Our app uses React for the frontend, which interacts with the RAG backend.
- **FastAPI (Backend):** We use FastAPI to handle RESTful API calls for processing user queries.
- **FAISS (Vector Search):** FAISS is used for searching through the vector embeddings generated from Wikipedia articles.

### Installation Steps

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/mollyiverson/ACME10-HE-RAGApp.git
   cd ACME10-HE-RAGApp
   ```

2. **Install Backend Dependencies:**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate  
   # On Windows: `venv\Scripts\activate`
   # On Linux: `source venv/Scripts/activate`
   pip install -r requirements.txt
   ```
3. **Install Frontend Dependencies:**
- Download [Node.js (LTS)](https://nodejs.org/en)
   ```bash
   cd ../frontend
   npm install
   ```

4. **Run Backend:**
   ```bash
   cd ../backend
   python -m uvicorn app.main:app --reload
   ```

5. **Run Frontend:**
   ```bash
   cd ../frontend
   npm start
   ```

6. **Run Tests:**
   ```bash
   cd ACME10-HE-RAGApp
   pytest -s  # -s is optional if you want print statements to show
   ```

The application should now be running on `localhost` for both frontend and backend.


## Functionality

The RAG application allows users to enter queries and receive accurate, context-rich responses from a combination of vector search and knowledge graphs.

### Walkthrough

1. Open the application in your browser.
2. Input a question or query related to the Wikipedia dataset.
3. The application retrieves relevant information using vector embeddings.
4. The knowledge graph adds contextual insights to the response.
5. The LLM generates a coherent answer based on the retrieved data.

The chat interface supports query submission, response retrieval, and historical session saving for reference.

## Known Problems

- **Performance Degradation with Large Datasets:** With over 10,000 articles, there may be a slowdown during query processing. We are currently optimizing the indexing and retrieval process.
- **Error Handling with Knowledge Graph Queries:** If a SPARQL query to the knowledge graph fails, the system may return incomplete information.
- **Missing Responses:** In rare cases, the system might generate an "I don't know" response when the knowledge base doesn't have enough data to provide an accurate answer.

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## Additional Documentation

* [Project Abstract](docs/project-report/Project-Abstract.pdf)
* [Sprint reports](docs/sprint-reports/)
* User links

## License

See `LICENSE.txt` 
