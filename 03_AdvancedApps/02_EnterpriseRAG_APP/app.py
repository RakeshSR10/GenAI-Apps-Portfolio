import os
import streamlit as st
from llm import llm
from utils import load_pdf, advanced_parent_child_splitter
from rag_chain import create_enterprise_vector_store, retrieve_parent_context

st.set_page_config(page_title="Enterprise RAG Dashboard", page_icon="🏢", layout="wide")
st.title("🏢 Enterprise Parent-Child Retrieval System (RAG)")
st.markdown("This system indexes text using **High-Precision Child Chunks** for search matching, but reconstructs **Full Parent Sections** to ensure zero context loss.")

# Initialize persistent memory structures in session state
if "enterprise_db" not in st.session_state:
    st.session_state.enterprise_db = None
if "parent_map" not in st.session_state:
    st.session_state.parent_map = None
if "active_file" not in st.session_state:
    st.session_state.active_file = None

# Step 1: Secure Document Ingestion File Input Element
uploaded_file = st.file_uploader("Upload Corporate Knowledge Base Document (PDF)", type="pdf")

if uploaded_file is not None:
    # Reset indices if a completely new document is provided
    if st.session_state.active_file != uploaded_file.name:
        st.session_state.enterprise_db = None
        st.session_state.parent_map = None
        st.session_state.active_file = uploaded_file.name

    if st.session_state.enterprise_db is None:
        with st.spinner("Executing multi-tier parent-child document chunking..."):
            try:
                # Save file locally safely
                temp_filename = "temp_enterprise_doc.pdf"
                with open(temp_filename, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Load text, slice using the advanced strategy, and extract data matrices
                raw_docs = load_pdf(temp_filename)
                child_chunks, parent_storage_map = advanced_parent_child_splitter(raw_docs)
                
                # Persist both the database index and parent lookup mapping definitions
                st.session_state.enterprise_db = create_enterprise_vector_store(child_chunks)
                st.session_state.parent_map = parent_storage_map
                
                # FIX: Clean up local disk cache immediately after indexing
                if os.path.exists(temp_filename):
                    os.remove(temp_filename)
                
                st.success(f"Successfully processed! Generated {len(child_chunks)} Searchable Child Chunks linked to {len(parent_storage_map)} Large Context Parent Sections.")
            except Exception as e:
                st.error(f"Ingestion crashed: {str(e)}")
                st.session_state.active_file = None
    else:
        st.info("🏢 Document index maps loaded into system cache and ready.")

# Step 2: High-Precision Retrieval Search Workspace
if st.session_state.enterprise_db is not None:
    st.write("---")
    question = st.text_input("Ask a question about the document data:")
    
    if question:
        with st.spinner("Searching children indexes and synthesizing parent context blocks..."):
            # 1. Retrieve reconstructed un-cut parent sections
            enriched_context = retrieve_parent_context(
                st.session_state.enterprise_db, 
                st.session_state.parent_map, 
                question
            )
            
            # 2. Formulate strict contextual instruction prompt template
            prompt = f"""You are an elite Enterprise Data Analyst. Answer the question using the provided context blocks only.
Always answer comprehensively and retain professional names, dates, numbers, and metrics.
If you cannot verify the answer from the context block, say "The requested information is not located within the current database logs."

Provided Rich Context Sections:
{enriched_context}

Question: {question}
"""
            # 3. Invoke the Gemini generation step
            response = llm.invoke(prompt).content
            
            # 4. Display result and backend details side-by-side
            ans_col, context_col = st.columns(2)
            
            with ans_col:
                st.markdown("### 🤖 Synthesized Answer")
                st.success(response)
                
            with context_col:
                st.markdown("### 🔎 Retrieved Parent Context Audit")
                with st.expander("View Reconstructed Document Sections Shared with LLM", expanded=True):
                    st.text(enriched_context)
