# **Minutes of Meeting**

**Project Name**: ACME10-HE-RAGApp

**Client Name**: HackerEarth (CEO Vikas Aditya)

**Date**: 10/15/2024 

**Time**: 12 pm - 12:15pm PST

**Location**: Zoom

**Attendees**:
- Vikas Aditya
- Molly Iverson 
- Ethan Villalovoz
- Chandler Juego
- Adam Shtrikman

---

## **1. Agenda**
- Discussion of planned milestone.

---

## **2. Meeting Summary**

### Introduction:
- The project team (Ethan Villalovoz, Molly Iverson, Chandler Juego, and Adam Shtrikman) provided an update on the plan to expedite the development of a basic frontend.
- The client acknowledged that the team is making good progress.

### Client’s Requirements:
- The client recommends developing a complete pipeline, which includes integrating a vector database, querying the vector database, generating questions, and producing responses. Once this is in place, the team can scale up the amount of document input to enhance the model's quality, while still maintaining functionality with fewer documents.

### Key Discussion Points:
- **Discussion Point 1**: Requirements and Specifications Section Feedback: The client expressed satisfaction with the team's progress.
- **Discussion Point 2**: BERT Progress: Chandler successfully extracted the Parquet file and began embedding it using BERT. Due to compute limitations, he was able to embed data line by line and plans to organize the data by article. Chandler will explore GPU acceleration to improve performance on a larger dataset.
- **Discussion Point 3**: Timeline: The team incorporated buffer time this week in light of the upcoming deadline for the Solution Approach document.

### Decisions Made:
- It was decided that FAISS will be used as the vector search framework.


### Action Items:
- The client requested that each team member submit a brief summary of their roles to facilitate the client’s evaluation report on team performance by the end of this week.

---

## **3. Project Milestones Discussed**
- Solution Approach Section: The completed document is to be delivered by 10/20/2024.

---

## **4. Next Steps**
- Prioritize the completion of the Solution Approach Section document and assign related tasks to team members.
- Continue working on BERT on larger dataset and implementation with FAISS.

---

## **5. Next Meeting**
- **Date**: 10/22/2024
- **Time**: 12:00 pm PST
- **Location**: Zoom

---

**Meeting Notes Prepared By**: Adam Shtrikman
**Date**: 10/15/2024
