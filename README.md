# Quebec Bar Helper

## Overview
The Quebec Bar Helper is an AI assistant designed to help students study for the Barreau du Québec.
It answers legal questions using official legal materials only, such as the Civil Code, procedural notes,
and responsabilité civile documents.

Built with LangChain, FAISS, and OpenAI embeddings, the application functions like a specialized ChatGPT
that retrieves answers exclusively from a user-provided legal corpus.

---

## System Architecture

Raw Legal Texts (.txt)
        |
        v
RecursiveCharacterTextSplitter
(splits large documents)
        |
        v
OpenAIEmbeddings
(creates numerical vector representations)
        |
        v
FAISS Vector Store
(semantic database of legal text chunks)
        |
        v
Streamlit Web App
(user interface for querying the model)
        |
        v
GPT-4 Model
(answers using retrieved context)

---

## Folder Structure

quebec-bar-helper/
|
|-- data/
|   |-- Civil_Code/
|   |-- Responsabilite/
|   |-- Procedure/
|
|-- vector_db/             # FAISS index (index.faiss + index.pkl)
|-- build_db.py            # Builds the vector database from text files
|-- app.py                 # Streamlit chatbot interface
|-- .env                   # Contains OpenAI API key (not committed)
|-- README.md

---

## How It Works

1. Data Ingestion  
All .txt files located in the data directory and its subfolders are read and concatenated.

2. Text Chunking  
Documents are split into overlapping chunks of approximately 1000 characters with a 100-character overlap
using RecursiveCharacterTextSplitter.

3. Embedding Generation  
Each text chunk is converted into a numerical vector using the OpenAI embeddings model
(text-embedding-3-small).

4. Vector Indexing  
The resulting vectors are stored locally using FAISS in the vector_db directory.

5. Question Answering  
The Streamlit application loads the FAISS index, retrieves the most semantically relevant text chunks,
passes them as context to GPT-4, and generates grounded legal answers based on retrieved materials.

---

## Environment Setup

Create a .env file in the project root containing:

OPENAI_API_KEY=sk-...

Install dependencies and run the application:

pip install -r requirements.txt
python build_db.py
streamlit run app.py

---

## Next Phase

Phase 2 will extend the project with a Practice Exam Generator that fine-tunes a lightweight OpenAI model
(gpt-3.5-turbo) on past Quebec Bar examinations to generate realistic multiple-choice practice questions.
