Antopic is a RAG (Retrieval-Augmented Generation) app I worked on when I first got my hands on the gpt3.5-turbo and 4 APIs, roughly April/May 2023. It is a prototype leaning heavily on dependencies, but is capable of some short-medium length video/audio ingestion. 

Users can: 
* create a "Topic" 
* import/ingest "Content" to the topic (originally intended for podcast video & audio) that can be used to provide better context to an LLM so a user can "Chat with the content" by asking questions and receive responses that refer to specific content in the audio or video.

The app was written with a Django backend, Celery workers for video/audio/document ingestion & a Vue.js frontend. It made use of langchain Retrieval libraries which make the RAG model pretty much OOB. 

The infrastructure the app relies on is: 

* A backend LLM service (Implemented here with OpenAI's text completion API)
* A semantic vector embedding service (Imeplmented here with OpenAI embedding model)
* A backend vector store (implemented here with pineconeDB)
* A DB for users / chat storage - using MongoDB
* A redis cache for the (celery) ingestion worker queue
* An identity provider for auth (Auth0 used here) 

The application has three components:

* Backend API  - CRUD for topics & content, and the chat endpoint  
* Celery worker(s) - content ingestion jobs
* Frontend Vue.js Site (served statically) - frontend UI 

