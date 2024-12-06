# Sprint 3 Report (11/6/2024 - 12/5/2024)

[Sprint 3 Video Link](https://www.youtube.com/watch?v=whDkO0fSobI&feature=youtu.be)

---

## What's New (User Facing)
* Fully integrated query-processing pipeline, allowing end-to-end functionality for vector search, knowledge graph querying, and response generation.
* Improved response accuracy through FAISS-enhanced vector search and cosine similarity-based query refinement.
* A functional alpha prototype with backend and React-based frontend integration, demonstrating RAG application capabilities.

---

## Work Summary (Developer Facing)
This sprint focused on pipeline integration, component enhancements, and automation. The LLM was implemented to generate coherent responses from combined vector search and knowledge graph outputs. Vector search functionality was extended with a small subset of Wikipedia data to refine retrieval results. The CI/CD pipeline was set up to streamline testing, ensuring development consistency. The NLP and KG modules were integrated into the pipeline and connected to the React frontend for seamless user interactions. Refactoring efforts also improved the organization of file folders for maintainability. Despite some challenges in ensuring compatibility during integration, all major pipeline components are now operational.

---

## Unfinished Work
* Full-scale embedding generation for the entire Wikipedia dataset remains pending due to computational limitations.
* Refinement of NLP capabilities to better handle complex or ambiguous queries.

---

## Completed Issues/User Stories
Here are links to the issues and user stories completed in this sprint:

- [Integrate NLP and KG into Pipeline and connect to React](https://github.com/mollyiverson/ACME10-HE-RAGApp/issues/61)  
- [Implement vector search with small subset of Wiki data](https://github.com/mollyiverson/ACME10-HE-RAGApp/issues/62)  
- [Implement LLM component](https://github.com/mollyiverson/ACME10-HE-RAGApp/issues/63)  
- [Integration of NLP and KG in the RAG pipeline](https://github.com/mollyiverson/ACME10-HE-RAGApp/issues/64)  
- [Set up CI/CD Pipeline for Testing Automation](https://github.com/mollyiverson/ACME10-HE-RAGApp/issues/65)  
- [Add team bio and project role information](https://github.com/mollyiverson/ACME10-HE-RAGApp/issues/68)  
- [Write Future Work section in project report](https://github.com/mollyiverson/ACME10-HE-RAGApp/issues/69)  
- [Write alpha prototype description](https://github.com/mollyiverson/ACME10-HE-RAGApp/issues/71)  


---

## Incomplete Issues/User Stories
There are no incomplete issues or user stories for this sprint. All planned work has been successfully completed.

---

## Code Files for Review
Please review the following files for quality and feedback:
- [backend/app/handlers/embeddings_handler.py](https://github.com/mollyiverson/ACME10-HE-RAGApp/blob/main/backend/app/handlers/embeddings_handler.py) – Manages the embedding generation process.
- [backend/app/handlers/llm_handler.py](https://github.com/mollyiverson/ACME10-HE-RAGApp/blob/main/backend/app/handlers/llm_handler.py) – Handles interactions with the large language model.
- [backend/app/handlers/vector_search_handler.py](https://github.com/mollyiverson/ACME10-HE-RAGApp/blob/main/backend/app/handlers/vector_search_handler.py) – Implements vector search functionality using FAISS.
- [backend/app/models/basic_query.py](https://github.com/mollyiverson/ACME10-HE-RAGApp/blob/main/backend/app/models/basic_query.py) – Defines the structure for basic query models.
- [backend/app/models/vector_search_query.py](https://github.com/mollyiverson/ACME10-HE-RAGApp/blob/main/backend/app/models/vector_search_query.py) – Represents models for vector search queries.
---

## Retrospective Summary
### What Went Well:
* Successfully implemented and integrated key components (VS, KG, NLP, LLM) into the pipeline.
* Robust CI/CD pipeline ensured efficient automated testing.
* Demonstrated alpha prototype with fully integrated functionality.

### What Needs Improvement:
* Enhance NLP for handling complex and ambiguous queries.

### Planned Changes for the Next Sprint:
* Embedding generation scalability to process the entire dataset efficiently using chunking.
* Refine the retrieval process by further optimizing vector search and knowledge graph integration.
* Conduct comprehensive system-level testing with varied query inputs.
* Improve frontend capabilities for better user interaction.
