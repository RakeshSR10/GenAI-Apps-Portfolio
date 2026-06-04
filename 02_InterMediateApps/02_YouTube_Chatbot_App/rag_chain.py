import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

# 1. Dynamically locate the global .env file at the workspace root level (4 levels up)
root_dir = Path(__file__).resolve().parents[4] 
env_path = root_dir / '.env'

# 2. Load the global .env file with override enabled
load_dotenv(dotenv_path=env_path, override=True)

# Fetch API key for the embeddings generator engine
api_key = os.getenv("GOOGLE_API_KEY")

# Embeddings Model Configuration using the latest standard
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004",
    google_api_key=api_key
)

def create_vector_store(docs):
    """Builds an in-memory local FAISS database from transcript chunks."""
    db = FAISS.from_documents(docs, embeddings)
    return db

def get_context(db, question):
    """Searches the video transcript for relevant context."""
    results = db.similarity_search(question, k=4)
    context = "\n\n".join([doc.page_content for doc in results])
    return context
