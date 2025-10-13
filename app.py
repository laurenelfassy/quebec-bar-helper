import streamlit as st
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import os

# --- Load API key ---
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# --- Streamlit UI ---
st.set_page_config(page_title="Quebec Bar Study Helper", page_icon="⚖️")
st.title("⚖️ Quebec Bar Study Helper")
st.write("✅ Using pre-loaded Quebec Bar knowledge base")

# --- Load prebuilt database ---
embeddings = OpenAIEmbeddings()
db = FAISS.load_local("vector_db", embeddings, allow_dangerous_deserialization=True)
retriever = db.as_retriever(search_kwargs={"k": 3})

qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model="gpt-4-turbo", temperature=0.2),
    chain_type="stuff",
    retriever=retriever
)

# --- Question input ---
query = st.text_input("Ask a question about your notes:")
if query:
    response = qa_chain.run(query)
    st.write("### Answer:")
    st.write(response)
