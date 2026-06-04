import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

# 1. Dynamically locate the global .env file at the workspace root level (4 levels up)
root_dir = Path(__file__).resolve().parents[3]
env_path = root_dir / '.env'

# 2. Load the global .env file with override enabled
load_dotenv(dotenv_path=env_path, override=True)

# Fetch API key for the embeddings generator engine
api_key = os.getenv("GOOGLE_API_KEY")

# Embeddings Model Configuration using the latest text-embedding-004 standard
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004",
    google_api_key=api_key
)

def create_enterprise_vector_store(child_chunks):
    """Indexes high-precision child fragments into a local FAISS vector store."""
    db = FAISS.from_documents(child_chunks, embeddings)
    return db

def retrieve_parent_context(db, parent_storage_map, question):
    """
    Advanced Retrieval: Searches child chunks, then instantly maps 
    their references back to return the complete Parent Document context.
    """
    # 1. Search for top 6 matching miniature child blocks to capture precise details
    child_results = db.similarity_search(question, k=6)
    
    retrieved_parent_texts = []
    seen_parent_ids = set()
    
    # 2. Map child results back to their parent chunks
    for child in child_results:
        parent_id = child.metadata.get("parent_id")
        
        # Ensure we don't fetch duplicate parent blocks if multiple children match
        if parent_id and parent_id not in seen_parent_ids:
            seen_parent_ids.add(parent_id)
            # Retrieve the full, uncut parent text from our memory storage map
            full_parent_text = parent_storage_map.get(parent_id)
            if full_parent_text:
                retrieved_parent_texts.append(full_parent_text)
                
    # 3. Merge the rich parent context blocks together cleanly
    context = "\n\n--- Document Section ---\n\n".join(retrieved_parent_texts)
    return context
