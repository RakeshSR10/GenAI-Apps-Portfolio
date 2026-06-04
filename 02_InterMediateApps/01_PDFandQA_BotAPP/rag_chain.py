import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

# 1. Dynamically locate the global .env file at the workspace root level
root_dir = Path(__file__).resolve().parents[3] 
env_path = root_dir / '.env'

# 2. Load the global .env file with override enabled
load_dotenv(dotenv_path=env_path, override=True)

# Fetch API key for the embeddings generator engine
api_key = os.getenv("GOOGLE_API_KEY")

# Embeddings Model Configuration
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004",  # Updated to Google's latest, highly accurate text embedding standard [2026]
    google_api_key=api_key
)

def create_vector_store(docs):
    """Creates a local in-memory FAISS vector store database index."""
    db = FAISS.from_documents(docs, embeddings)
    return db

def get_context(db, question):
    """Finds and extracts the top 3 semantically close context blocks."""
    results = db.similarity_search(question, k=3)
    context = "\n\n".join([doc.page_content for doc in results])
    return context
