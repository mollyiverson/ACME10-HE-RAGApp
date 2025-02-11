# Sprint 4 Report (1/10/2025 - 2/10/2025)

[Sprint 4 Video Link](#)

---

## What's New (User Facing)
* Switched LLM from LLaMA to ChatGPT, improving response accuracy and contextual understanding.
* Implemented system performance testing, logging execution times for each pipeline component.
* Enhanced document embedding process by implementing chunking, improving vector search efficiency.
* Integrated chunking into the vector search pipeline to enhance retrieval performance.

---

## Work Summary (Developer Facing)
This sprint focused on improving the system’s efficiency, response accuracy, and performance evaluation. The LLM component was migrated from LLaMA to ChatGPT for better response generation. System testing was improved by implementing logging for the execution times of different components in the pipeline, identifying bottlenecks. The dataset chunking process was integrated into the embedding generation, allowing more efficient processing and retrieval of relevant document sections. 

Additionally, we refined our vector search system by improving query response handling, ensuring consistency in the integration between the LLM, vector search, and knowledge graph modules. These changes have significantly improved both system performance and user experience.

---

## Unfinished Work
* Further fine-tuning of the ChatGPT response formatting to align with previous LLaMA-generated outputs.
* Optimization of chunking strategy to balance retrieval accuracy and efficiency.
* Expanding dataset embedding coverage beyond Wikipedia to increase system knowledge.

---

## Completed Issues/User Stories
Here are links to the issues and user stories completed in this sprint:

- [Switch LLM from LLaMA to ChatGPT](https://github.com/mollyiverson/ACME10-HE-RAGApp/issues/76)  
- [Implement system performance testing](https://github.com/mollyiverson/ACME10-HE-RAGApp/issues/77)  
- [Implement chunking for vector search](https://github.com/mollyiverson/ACME10-HE-RAGApp/issues/78)  
- [System Testing by Timing Components](https://github.com/mollyiverson/ACME10-HE-RAGApp/issues/79)  
- [Chunking Dataset During Embedding](https://github.com/mollyiverson/ACME10-HE-RAGApp/issues/81)  

---

## Incomplete Issues/User Stories
- Optimization of chunking approach for embeddings.
- Expansion of the vector search dataset to include additional sources beyond Wikipedia.
- Further refinement of LLM response structuring.

---

## Code Files for Review
Please review the following files for quality and feedback:
- [backend/app/handlers/llm_handler.py](https://github.com/mollyiverson/ACME10-HE-RAGApp/blob/main/backend/app/handlers/llm_handler.py) – Handles ChatGPT integration for response generation.
- [backend/app/handlers/vector_search_handler.py](https://github.com/mollyiverson/ACME10-HE-RAGApp/blob/main/backend/app/handlers/vector_search_handler.py) – Implements vector search enhancements.
- [backend/app/handlers/system_testing.py](https://github.com/mollyiverson/ACME10-HE-RAGApp/blob/main/backend/app/handlers/system_testing.py) – Logs execution times for system performance testing.
- [backend/app/data_processing/embedding_chunking.py](https://github.com/mollyiverson/ACME10-HE-RAGApp/blob/main/backend/app/data_processing/embedding_chunking.py) – Implements chunking for document embeddings.

---

## Retrospective Summary
### What Went Well:
* Successfully integrated ChatGPT for improved response quality.
* Performance testing provided valuable insights into system bottlenecks.
* Chunking implementation significantly improved document retrieval accuracy.

### What Needs Improvement:
* Fine-tuning of ChatGPT responses to maintain consistent output formatting.
* Further testing and optimization of dataset chunking to improve efficiency.
* Expanding dataset coverage to increase information retrieval capabilities.

### Planned Changes for the Next Sprint:
* Final optimizations to LLM query structuring for improved response coherence.
* Expansion of vector search capabilities to additional document sources.
* Further improvements to chunking methods to enhance retrieval efficiency.
* Conducting final testing and preparing for project deployment.
