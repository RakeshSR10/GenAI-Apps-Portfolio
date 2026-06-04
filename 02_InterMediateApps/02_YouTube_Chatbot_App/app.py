import os
import streamlit as st
from llm import llm
from utils import load_youtube_transcript, split_docs
from rag_chain import create_vector_store, get_context
from memory import Memory

st.set_page_config(page_title="YouTube Chat Bot", page_icon="🎬")
st.title("🎬 YouTube Video Transcript Q&A Bot (RAG)")

# Maintain separate session state trackers safely across execution reruns
if "yt_db" not in st.session_state:
    st.session_state.yt_db = None
if "current_video" not in st.session_state:
    st.session_state.current_video = None
if "yt_memory" not in st.session_state:
    st.session_state.yt_memory = Memory()

# Wrap the video input in a form container to guarantee page refreshes on submit
with st.form("video_indexer_form"):
    video_url = st.text_input("Paste YouTube Video URL here :-")
    submit_button = st.form_submit_button("Index Video Content")

# Process indexing and save the state permanently inside session_state
if submit_button and video_url:
    if st.session_state.current_video != video_url:
        st.session_state.yt_db = None
        st.session_state.current_video = video_url
        st.session_state.yt_memory = Memory()

    with st.spinner("Processing video transcript details..."):
        try:
            docs = load_youtube_transcript(video_url)
            chunks = split_docs(docs)
            st.session_state.yt_db = create_vector_store(chunks)
            st.success("Indexed Successfully!")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# FIX: Keep this section independent from the button press so it stays visible on reruns
if st.session_state.yt_db is not None:
    st.write("---")
    st.info("🟢 Video transcript loaded and ready for questions.")
    
    # We use a unique key for the text input to ensure state synchronization
    question = st.text_input("Ask about the video:", key="user_question_input")
    
    if question:
        with st.spinner("Analyzing video transcript content with Gemini 2.5 Flash..."):
            # Gather matching semantic context from FAISS
            context = get_context(st.session_state.yt_db, question)
            
            # Extract full history timeline logs
            history_logs = st.session_state.yt_memory.get()
            formatted_history = "\n".join([f"{chat['role']}: {chat['msg']}" for chat in history_logs])
            
            # Formulate prompt template
            prompt = f"""Answer the question using the provided video transcript context only.
If the answer cannot be found in the context, say "The video does not cover this information."

Conversation History:
{formatted_history}

Video Transcript Context:
{context}

Question: {question}
"""
            # Generate final result from your Gemini model connection
            response = llm.invoke(prompt).content
            
            # Append interaction loops back to memory arrays
            st.session_state.yt_memory.add("User", question)
            st.session_state.yt_memory.add("Bot", response)
            
            # Output to screen
            st.write("🤖 Answer:")
            st.success(response)

    # FIX: Moved outside the 'if question' block so history stays visible after you hit Enter
    if st.session_state.yt_memory.get():
        st.write("---")
        with st.expander("Show Complete Conversation Logs", expanded=True):
            for chat in st.session_state.yt_memory.get():
                if chat['role'] == "User":
                    st.markdown(f"👤 **You:** {chat['msg']}")
                else:
                    st.markdown(f"🤖 **Bot:** {chat['msg']}")
                st.write("") # Add spacing between rows
