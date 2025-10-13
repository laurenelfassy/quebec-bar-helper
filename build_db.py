from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

folder = "data"
text_data = ""

# ✅ Walk through all subfolders and read every .txt file
for root, _, files in os.walk(folder):
    for file_name in files:
        if file_name.endswith(".txt"):
            path = os.path.join(root, file_name)
            with open(path, "r", encoding="utf-8") as f:
                text_data += f.read() + "\n"

print("✅ Text collection complete.")

# Split text into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = splitter.split_text(text_data)
print(f"✅ Number of chunks: {len(chunks)}")

# Build embeddings + FAISS index
embeddings = OpenAIEmbeddings()
db = FAISS.from_texts(chunks, embeddings)
db.save_local("vector_db")

print("✅ Knowledge base built and saved to /vector_db")
