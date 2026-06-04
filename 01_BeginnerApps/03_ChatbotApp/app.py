import streamlit as st
from llm import llm
from memory import ChatMemory

st.set_page_config(page_title="Gemini Chatbot", layout="centered")
st.title("🤖 Gemini AI Chatbot")

# memory init
if "memory" not in st.session_state:
    st.session_state.memory = ChatMemory(limit=10)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Clear chat button
if st.button("🧹 Clear Chat"):
    st.session_state.memory.clear()
    st.session_state.messages = []
    st.rerun()

# display history
for msg in st.session_state.messages:
    if msg["role"] == 'user':
        st.chat_message('user').write(msg['content'])
    else:
        st.chat_message('assistant').write(msg['content'])

# input box
user_input = st.chat_input("Type your message...")

if user_input:
    # Immediately display user message in the UI stream
    with st.chat_message("user"):
        st.write(user_input)

    # store user msg
    st.session_state.memory.add_user(user_input)
    st.session_state.messages.append({'role': 'user', 'content': user_input})

    # build messages for LLM and fetch response
    with st.chat_message("assistant"):
        messages = st.session_state.memory.get()
        response = llm.invoke(messages).content
        st.write(response)

    # store ai msg
    st.session_state.memory.add_ai(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

    # refresh state securely
    st.rerun()
