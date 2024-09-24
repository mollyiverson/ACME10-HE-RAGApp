# **Minutes of Meeting**

**Project Name**: ACME10-HE-RAGApp 

**Client Name**: HackerEarth (CEO Vikas Aditya) 

**Date**: 09/24/2024 

**Time**: 12 pm - 12:30 pm PST

**Location**: Zoom

**Attendees**:
- Vikas Aditya  
- Molly Iverson
- Ethan Villalovoz
- Chandler Juego
- Adam Shtrikman

---

## **1. Agenda**
-  Feedback about project background section, dataset and RAG discussion, project plan advice

---

## **2. Meeting Summary**

### Introduction:
- The project team (Molly Iverson, Ethan Villalovoz, Chandler Juego, and Adam Shtrikman) provided an overview of the ACME10-HE-RAGApp project and current progress
- The project aims to develop a Retrieval-Augmented Generation (RAG) application using a Simple Wikipedia dataset, with the potential to scale to larger  or custom datasets
- Vikas Aditya, representing HackerEarth, is the primary stakeholder, providing feedback and guidance

### Client’s Requirements:
- The client clarified that the project should leverage existing knowledge graphs instead of creating new ones
- The RAG application will initially use the Simple Wikipedia dataset, with plans to eventually transition to full Wikipedia or private datasets
- The system should be able to handle Apache Parquet files and focus on embedding and vector search techniques for efficient data querying and retrieval

### Key Discussion Points:
- **Discussion Point 1**: Project background section feedback from the client
    - Client approves the document but would like us to change the phrase "create a knowledge graph". It's better to use pre-existing ones
- **Discussion Point 2**: Dataset access granted from client along with Python scripts to interact with it
    - Dataset is Simple Wikipedia, which has shorter sentences and is well-suited for RAG applications. Once this is mastered, we can move on to the full Wikipedia
    - Format is a Apache Parquet file
    - [Dataset link](https://drive.google.com/file/d/17gLFB6RwwcF5CkrQK13sXWdPJFD4QQQ2/view?usp=drive_link)
    - [Python tutorial 1](https://inside-machinelearning.com/en/open-parquet-python/) and [Python tutorial 2](https://pypi.org/project/parquet/)
- **Discussion Point 3**: Best use for RAG applications
    - RAG is used best for private/custom datasets. Can't ask ChatGBT for this
        - Example uses: chatbots for internal company support, customer service representative, sales representative, engineers regarding the application domain
    - Our project becomes more powerful when we can swap out the public Wikipedia dataset for a private one

### Decisions Made:
- Client approval of project description section
- Agreement for project team to create a mini project plan outlining 10-12 milestones for the semester 

### Action Items:
- Project team to revise project description based on client feedback - Due by 09/25/2024
- Project team to plan 10-12 project milestones for the semester and submit to client for feedback - Due by 09/30/2024
- Project team to write requirements section and submit to client for feedback - Due by 09/30/2024

---

## **3. Project Milestones Discussed**
- Requirements section to be completed by 09/30/2024
- Sprint 1 to be completed by 10/05/2024

---

## **4. Next Steps**
- Draft requirements section by Friday and finalize by Sunday
- Think about using embeddings for vector searching and querying using languages like SparkQL

---

## **5. Next Meeting**
- **Date**: 10/01/2024  
- **Time**: 12 pm PST 
- **Location**: Zoom 

---

**Meeting Notes Prepared By**: Molly Iverson
**Date**: 09/24/2024
