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

The LLaMA 2.7b model doesn't work on Molly's computer and exhausts memory and CPU. Switching to a different model is important. The LLaMA model takes 5-10 minutes on Chandler's computer.

**Potential Bottlenecks**
- LLaMA 2.7b has 70 billion parameters
- Not storing chunks/documents or embeddings/indexes in a database
- Not chunking yet
- Local issues with LLM
- Slow local computer 

---

#### Change 1: Switching to ChatGPT and Chunking with Embeddings
| Component          | Call 1 (ms) | Call 2 (ms) | Call 3 (ms) | Average (ms) |
|---------------------|-------------|-------------|-------------|--------------|
| NLP Handler         |341.40       |34.80        |345.30       |240.50        |
| Knowledge Graph     |1149.70      |931.70       |2112.30      |1397.90       |
| Vector Search       |1924.70      |1747.40      |1753.50      |1808.53       |
| LLM                 |2405.30      |2866.90      |3245.50      |2839.23       |
| **Total**           |5821.90      |5581.30      |7457.50      |6286.90       |

---

#### Final Stats
| Component          | Call 1 (ms) | Call 2 (ms) | Call 3 (ms) | Average (ms) |
|---------------------|-------------|-------------|-------------|--------------|
| NLP Handler         |36.40        |27.40        |36.40        |33.40         |
| Knowledge Graph     |1498.20      |1392.70      |1212.30      |1367.73       |
| Vector Search       |3717.20      |4672.20      |4011.20      |4133.53       |
| LLM                 |2527.00      |1884.80      |1827.29      |2079.70       |
| **Total**           |7779.70      |7977.60      |7087.90      |7615.07       |

---

### Notes
- Include any observations or anomalies encountered during testing
- Use the same prompt for consistency unless specifically testing prompt variability
- Update this document for each significant change and re-testing cycle


