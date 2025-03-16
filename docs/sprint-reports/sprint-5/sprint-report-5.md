# Sprint 5 Report (2/11/2025 - 3/17/2025)

[Sprint 5 Video Link](https://youtu.be/tmZtU776Xmw)

---

## What's New (User Facing)
- Successfully embedded and indexed the full **Wikipedia dataset**, improving knowledge retrieval capabilities.
- Optimized **vector search ranking** by implementing **threshold filtering** and switching to a **SentenceTransformer model**, enhancing search relevance.
- Developed a **CI/CD pipeline** for streamlined app deployment, making installation and updates easier.
- Integrated **custom dataset embeddings** (e.g., class notes) to test adaptability and specialization of the RAG model.
- Enhanced **quality assurance** by testing a wide variety of queries and refining the UI for better user experience.

---

## Work Summary (Developer Facing)
This sprint focused on **scaling up dataset processing**, optimizing search performance, and improving **app deployment and usability**.

- **Ethan** worked on generating and indexing **large-scale Wikipedia embeddings**, handling over **5GB** of data, and refining chunking strategies to balance retrieval accuracy and efficiency.
- **Chandler** improved **vector search** accuracy, tested different **query optimization techniques**, and conducted **QA testing** by evaluating the system with diverse question types.
- **Molly** packaged the application with **Docker** and set up a **CI/CD pipeline** for seamless deployment, ensuring easy setup and updates across different systems.
- **Adam** integrated a **custom dataset** into the embedding workflow, allowing **domain-specific embeddings** for more personalized RAG responses.
- **All Team Members** contributed to writing and refining the **final project report**, recording client meetings, and preparing for the **poster presentation and research paper**.

---

## Unfinished Work
- Further refinement of **vector search ranking filters** for improved accuracy.
- Additional **testing with diverse queries** to evaluate performance across different dataset embeddings.
- Final optimization of **custom dataset embeddings** for specialized use cases.

---

## Completed Issues/User Stories
Here are links to the issues and user stories completed in this sprint:

- [Embed Full Wikipedia Dataset](https://github.com/mollyiverson/ACME10-HE-RAGApp/issues/88)  
- [Improve Vector Search Ranking](https://github.com/mollyiverson/ACME10-HE-RAGApp/issues/86)  
- [Implement CI/CD Pipeline for App Deployment](https://github.com/mollyiverson/ACME10-HE-RAGApp/issues/87)  
- [Integrate Custom Dataset Embeddings](https://github.com/mollyiverson/ACME10-HE-RAGApp/issues/80) 

---

## Incomplete Issues/User Stories
- Further **vector search refinement** and **threshold-based ranking adjustments**.
- Expanding **test coverage for dataset embeddings** with more diverse question types.
- Additional **performance evaluations** for different embedding strategies.

---

## Code Files for Review
Please review the following files for quality and feedback:

- [backend/app/handlers/embeddings_handler.py](https://github.com/mollyiverson/ACME10-HE-RAGApp/blob/main/backend/app/handlers/embeddings_handler.py) – Handles large dataset embedding generation.  
- [backend/app/handlers/vector_search_handler.py](https://github.com/mollyiverson/ACME10-HE-RAGApp/blob/main/backend/app/handlers/vector_search_handler.py) – Implements vector search ranking optimizations.  

---

## Retrospective Summary
### What Went Well:
* **Successfully embedded the full Wikipedia dataset**, enabling broader knowledge retrieval.  
* **Implemented CI/CD deployment**, making it easier to install and update the application.  
* **Improved vector search accuracy**, ensuring **higher-quality responses** to user queries.  
* **Integrated a custom dataset**, expanding RAG model capabilities beyond Wikipedia.  

### What Needs Improvement:
* Further fine-tuning of **vector search ranking filters** for **better search precision**.  
* Additional **query-based testing** for evaluating different dataset embeddings.  
* Finalizing **performance optimization strategies** before deployment.  

### Planned Changes for the Next Sprint:
* **Refine vector search filtering and expand query testing.**  
* **Continue embedding evaluation and verify response performance.**  
* **Prepare for final poster and client presentations.**  
* **Finalize research paper and document key findings.**
