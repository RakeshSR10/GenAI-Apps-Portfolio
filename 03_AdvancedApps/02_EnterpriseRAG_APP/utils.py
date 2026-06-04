import uuid
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def load_pdf(file_path):
    """Loads a local PDF file and extracts raw text pages."""
    loader = PyPDFLoader(file_path)
    return loader.load()

def advanced_parent_child_splitter(docs):
    """
    Advanced Strategy: Splits documents into large parent blocks,
    then subdivides them into small child chunks for high-accuracy searches.
    """
    # 1. Define splitting metrics
    parent_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=200)
    child_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=40)
    
    parent_docs = parent_splitter.split_documents(docs)
    
    final_child_chunks = []
    parent_storage_map = {}
    
    # 2. Process multi-tier mapping references
    for p_doc in parent_docs:
        # Generate a unique tracking ID for the parent block
        parent_id = str(uuid.uuid4())
        
        # Save parent text securely to our dictionary map tracking layout
        parent_storage_map[parent_id] = p_doc.page_content
        
        # Subdivide this specific parent block text down into small child blocks
        sub_child_chunks = child_splitter.split_text(p_doc.page_content)
        
        for c_text in sub_child_chunks:
            # Create a new document piece where the metadata points straight to the parent ID
            child_doc = Document(
                page_content=c_text,
                metadata={"parent_id": parent_id, "source": p_doc.metadata.get("source", "Unknown")}
            )
            final_child_chunks.append(child_doc)
            
    return final_child_chunks, parent_storage_map
