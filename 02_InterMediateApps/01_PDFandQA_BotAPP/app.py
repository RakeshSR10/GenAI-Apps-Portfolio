import os
import streamlit as st
from llm import llm
from utils import load_pdf, split_docs
from rag_chain import create_vector_store, get_context
from memory import Memory

st.set_page_config(page_title="PDF Q&A Bot", page_icon="📄")
st.title("📄 Intermediate PDF Q&A Bot (RAG)")

# Maintain session state keys across execution cycles
if "db" not in st.session_state:
    st.session_state.db = None
if "current_file" not in st.session_state:
    st.session_state.current_file = None
if "bot_memory" not in st.session_state:
    st.session_state.bot_memory = Memory()

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file is not None:
    if st.session_state.current_file != uploaded_file.name:
        st.session_state.db = None
        st.session_state.current_file = uploaded_file.name
        st.session_state.bot_memory = Memory()

    if st.session_state.db is None:
        with st.spinner("Processing PDF chunks and embedding into FAISS..."):
            with open("sample.pdf", "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            docs = load_pdf("sample.pdf")
            chunks = split_docs(docs)
            st.session_state.db = create_vector_store(chunks)
            st.success("PDF Content Indexed Successfully!")
    else:
        st.info("Document context loaded and ready.")

question = st.text_input("Ask a Question :-")

if question:
    if st.session_state.db is None:
        st.warning("Please upload and index a PDF file first.")
    else:
        with st.spinner("Searching database index and executing prompt..."):
            context = get_context(st.session_state.db, question)
            history_logs = st.session_state.bot_memory.get()
            formatted_history = "\n".join([f"{chat['role']}: {chat['msg']}" for chat in history_logs])
            
            prompt = f"""Answer the question using the provided context only.
If the answer cannot be found in the context, say "I cannot find the answer in the document."

Conversation History:
{formatted_history}

Context:
{context}

Question: {question}
"""
            response = llm.invoke(prompt).content
            
            st.session_state.bot_memory.add("User", question)
            st.session_state.bot_memory.add("Bot", response)
            
            st.write("🤖 Answer:")
            st.success(response)

if st.session_state.bot_memory.get():
    with st.expander("Show Chat History Logs"):
        for chat in st.session_state.bot_memory.get():
            st.markdown(f"**{chat['role']}:** {chat['msg']}")
