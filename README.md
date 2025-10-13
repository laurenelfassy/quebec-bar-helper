# quebec-bar-helper
OVERVIEW
The Quebec Bar Helper is an AI assistant designed to help students study for the Barreau du Québec.
It can answer legal questions using official materials such as the Civil Code, procedure notes, and responsabilité civile documents.
Built with LangChain, FAISS, and OpenAI embeddings, the app functions like a specialized ChatGPT that only draws knowledge from the user-provided legal corpus.

SYSTEM ARCHITECTURE 

[Raw Legal Texts (.txt)]
       │
       ▼
RecursiveCharacterTextSplitter
(splits large documents)
       │
       ▼
OpenAIEmbeddings
(creates numerical vector representations)
       │
       ▼
FAISS Vector Store
(semantic database of legal text chunks)
       │
       ▼
Streamlit Web App
(user interface for querying the model)
       │
       ▼
GPT-4 Model
(answers using retrieved context)

FOLDER STRUCTURE

quebec-bar-helper/
│
├── data/
│   ├── Civil_Code/
│   ├── Responsabilite/
│   └── Procedure/
│
├── vector_db/             ← FAISS index (index.faiss + index.pkl)
├── build_db.py            ← Builds the vector database from text files
├── app.py                 ← Streamlit chatbot interface
├── .env                   ← Contains your OpenAI API key
└── README.md

HOW IT WORKS

1. Data ingestion:
All .txt files in /data (and its subfolders) are read and concatenated.
2. Text chunking:
Each document is split into overlapping segments (≈1000 characters with 100 overlap) using RecursiveCharacterTextSplitter.
3. Embedding generation:
Each chunk is transformed into a numerical vector using the OpenAI Embeddings model (text-embedding-3-small).
4. Vector indexing:
FAISS stores these vectors locally in vector_db/.
5. Question answering:
The Streamlit app loads the FAISS database, retrieves the most semantically relevant chunks for each question, and sends them as context to GPT-4 Turbo to generate answers.

ENVIRONMENT SETUP
Create a .env file in the project root:
OPENAI_API_KEY=sk-...

Then install dependencies and run:
pip install -r requirements.txt
python build_db.py
streamlit run app.py

Next Phase
Phase 2 will extend the project with a Practice Exam Generator that fine-tunes a small OpenAI model (gpt-3.5-turbo) on past Quebec Bar exams to generate new, realistic multiple-choice questions.
