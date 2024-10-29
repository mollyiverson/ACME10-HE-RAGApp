# **Minutes of Meeting**

**Project Name**: ACME10-HE-RAGApp 

**Client Name**: HackerEarth (CEO Vikas Aditya) 

**Date**: 10/22/2024 

**Time**: 12 pm - 12:20 pm PST

**Location**: Zoom

**Attendees**:
- Vikas Aditya  
- Ethan Villalovoz
- Adam Shtrikman

---

## **1. Agenda**
- Feedback on the query structure formatting
- Clarification on project structures and overall progress
- Discussion of parallel development for Vector Search (VS) and Knowledge Graph (KG)
- Technical discussion on project components (embeddings, NLP techniques)

---

## **2. Meeting Summary**

### Introduction:
- The meeting began with the client expressing satisfaction with the query structure formatting.  
- No specific feedback was provided by the client, as they are happy with the current progress.

### Client’s Requirements:
- The client confirmed that the project’s Functional and Information Architecture Structure (FIASS) and other project structures look good.  
- The client asked if the team needed any assistance and confirmed that the team is currently self-sufficient, promising to ask for help if necessary.

### Key Discussion Points:
- **Discussion Point 1**: Query handling is on track. Users will type in a query via a text box, which will be used to trigger further processing.  
- **Discussion Point 2**: Parallel development of Vector Search (VS) and Knowledge Graph (KG) is recommended, with VS focusing on using embeddings to find relevant chunks from the database, and KG utilizing NLP techniques to extract relevant entities.  
- **Discussion Point 3**: The KG will have simple relationships, while the combined knowledge from both KG and VS will be passed to the chosen LLM for final processing.  
- **Discussion Point 4**: It was identified that an NLP technique box is missing after taking the query from the Chat Handler. This will need to be added to the flow.

### Decisions Made:
- Parallel development of Vector Search (VS) and Knowledge Graph (KG) will be pursued.  
- The team will implement simple relationships for the KG.  
- An NLP technique box will be added after taking the query from the Chat Handler.

### Action Items:
- **Action Item 1**: Add an NLP technique box after the Chat Handler in the project flow – Due by 25/10/2024.  
- **Action Item 2**: Begin implementing KG and VS modules in parallel – Due by 30/10/2024.  

---

## **3. Project Milestones Discussed**
- Completion of the NLP box and Chat Handler integration by 10/25/2024.  
- Parallel implementation of KG and VS components by 10/30/2024.  

---

## **4. Next Steps**
- Add the NLP technique box and finalize the architecture for the query flow.  
- Begin implementation of KG and VS in parallel.

---

## **5. Next Meeting**
- **Date**: 10/29/2024  
- **Time**: 12 pm PST 
- **Location**: Zoom 

---

**Meeting Notes Prepared By**: Ethan Villalovoz
**Date**: 10/22/2024
