from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Combine all your .txt files
folder = "data"
text_data = ""
for file_name in os.listdir(folder):
    if file_name.endswith(".txt"):
        with open(os.path.join(folder, file_name), "r", encoding="utf-8") as f:
            text_data += f.read() + "\n"

# Split text into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = splitter.split_text(text_data)

# Build embeddings + FAISS index
embeddings = OpenAIEmbeddings()
db = FAISS.from_texts(chunks, embeddings)
db.save_local("vector_db")

print("✅ Knowledge base built and saved to /vector_db")
