Antopic is a RAG (Retrieval-Augmented Generation) app for ingesting audio/video content and being able to query the information in it through an LLM interface

Users can: 
* create a "Topic" 
* import/ingest "Content" to the topic (originally intended for podcast video & audio) that can be used to provide better context to an LLM so a user can "Chat with the content" by asking questions and receive responses that refer to specific content in the audio or video.

The app was written with a Django backend, Celery workers for video/audio/document ingestion & a Vue.js frontend. It made use of langchain retrieval library which make the RAG model pretty much OOB. 

The infrastructure the app relies on is: 

* A backend LLM service (OpenAI's chat completion API)
* A semantic vector embedding service (OpenAI embedding model)
* A backend vector store (pineconeDB)
* A DB for users / chat storage - using MongoDB
* A redis cache for the (celery) ingestion worker queue
* An identity provider for auth (Auth0 used here) 

The application has three components:

* Backend API  - CRUD for topics & content, and the chat endpoint  
* Celery worker(s) - content ingestion jobs
* Frontend Vue.js Site (served statically) - frontend UI 

