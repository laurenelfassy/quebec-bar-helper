from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# === STEP 1: Load each file as a separate document ===
documents = []
folder = "data"

for root, _, files in os.walk(folder):
    for file_name in files:
        if file_name.endswith(".txt"):
            path = os.path.join(root, file_name)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    documents.append(
                        Document(
                            page_content=content,
                            metadata={"source": path}
                        )
                    )

print(f"✅ Loaded {len(documents)} documents")

if not documents:
    raise RuntimeError("❌ No documents found in /data")

# === STEP 2: Split documents safely ===
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

split_docs = splitter.split_documents(documents)
print(f"✅ Created {len(split_docs)} chunks")

# === STEP 3: Build embeddings with SAFE batch size ===
embeddings = OpenAIEmbeddings(chunk_size=50)

db = FAISS.from_documents(split_docs, embeddings)
db.save_local("vector_db")

print("🎉 FAISS index built successfully")
