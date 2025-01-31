# RAG Application Performance and System Testing

## Performance Testing

### Test Prompt
**Prompt:** "Who is Alan Turing?"

### Testing Methodology
1. Measure the average execution time (in milliseconds) for each component:
   - **NLP Handler**
   - **Knowledge Graph**
   - **Vector Search**
   - **LLM**
   - **Total Execution Time**
2. Each test will consist of three calls to the application with the specified prompt.
3. Record the average execution time of the three calls.
4. Re-test after implementing major changes (e.g., switching models, implementing chunking, etc.).

---

### Test Results

#### Initial Test
| Component          | Call 1 (ms) | Call 2 (ms) | Call 3 (ms) | Average (ms) |
|---------------------|-------------|-------------|-------------|--------------|
| NLP Handler         |552.30       |346.40       |552.00       |483.57        |
| Knowledge Graph     |1137.30      |1037.40      |1231.70      |1135.17       |
| Vector Search       |4418.30      |7159.30      |2973.20      |4850.27       |
| LLM                 |Not working  |Not working  |Not working  |Not working   |
| **Total**           |6107.9       |8543.1       |4756.9       |6469.3        |

The LLaMA 2.7b model doesn't work on Molly's computer and exhausts memory and CPU. Switching to a different model is important.

**Potential Bottlenecks**
- LLaMA 2.7b has 70 billion parameters
- Not storing chunks/documents or embeddings/indexes in a database
- Not chunking yet
- Local issues with LLM
- Slow local computer 

---

#### Change 1: Switching to ChatGBT
| Component          | Call 1 (ms) | Call 2 (ms) | Call 3 (ms) | Average (ms) |
|---------------------|-------------|-------------|-------------|--------------|
| NLP Handler         |             |             |             |              |
| Knowledge Graph     |             |             |             |              |
| Vector Search       |             |             |             |              |
| LLM                 |             |             |             |              |
| **Total**           |             |             |             |              |

---

#### Change 2: Switching to Chunking
| Component          | Call 1 (ms) | Call 2 (ms) | Call 3 (ms) | Average (ms) |
|---------------------|-------------|-------------|-------------|--------------|
| NLP Handler         |             |             |             |              |
| Knowledge Graph     |             |             |             |              |
| Vector Search       |             |             |             |              |
| LLM                 |             |             |             |              |
| **Total**           |             |             |             |              |

---

### Notes
- Include any observations or anomalies encountered during testing
- Use the same prompt for consistency unless specifically testing prompt variability
- Update this document for each significant change and re-testing cycle


