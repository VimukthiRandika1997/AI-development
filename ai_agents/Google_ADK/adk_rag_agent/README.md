# RAG Agent with Google ADK

In this project, A RAG agent is designed for querying information from the user uploaded documents (either Google Drive, Google Cloud Storage).

## Vertex AI RAG Engine

![Vertex AI RAG](https://cloud.google.com/static/vertex-ai/images/Vertex-RAG-Diagram.png)

This is a part of the Vertex AI platform which enables Retrieval Augmented Generation (RAG) to build context-aware LLM applications.

The platform has the following features:

- Fully managed Vector Store
- Support Real-time retrieval
- Seamless integration with Gemini models


## Typical Pipeline Overview

1. **Data Ingestion**: *collect data from various sources (local files, cloud storage, google drive)*
2. **Data Transformation**: *prepare the data for indexing by preprocessing (chunking)* 
3. **Embedding**: *split text into chunks to get numerical representation (embeddings)*
4. **Data Indexing**: *create an organized index(corpus) of the embeddings to facilitate efficient search and retrieval*
5. **Retrieval**: *search the indexed corpus to find the relevant information given a search query*
6. **Generation**: *Use the retrieved information as the context to generate accurate responses through LLM*

## Corpus

- A corpus is a collection of documents (sources of information) that is queried to retrieve relevant context for the response  generation by the LLM.

- Acts as the Knowledge Base (KB) for RAG

## Available Tools For the Agent

1. Add data 
2. Create corpus
3. Delete corpus
4. Delete document
5. Get corpus information
6. List available corpora
7. Query data

## How to run

```bash
# Create a virtual environment
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt

# For interactive web interface
adk web

# For interactive CLI interface
adk run rag_agent
```