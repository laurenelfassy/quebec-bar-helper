from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os

# Load your API key
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# === STEP 1: Read every .txt file inside /data and subfolders ===
folder = "data"
text_data = ""

for root, _, files in os.walk(folder):
    for file_name in files:
        if file_name.endswith(".txt"):
            path = os.path.join(root, file_name)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if len(content) > 0:
                    text_data += content + "\n"
                else:
                    print(f"⚠️ Skipping empty file: {path}")

print(f"✅ Total text length collected: {len(text_data):,} characters")

# === STEP 2: Split text into chunks ===
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = splitter.split_text(text_data)
print(f"✅ Number of chunks created: {len(chunks)}")

if len(chunks) == 0:
    print("❌ No chunks created! Check your .txt files or folder path.")
    exit()

# === STEP 3: Build embeddings and FAISS index ===
embeddings = OpenAIEmbeddings()
db = FAISS.from_texts(chunks, embeddings)
db.save_local("vector_db")

print("🎉 Knowledge base built and saved to /vector_db")
