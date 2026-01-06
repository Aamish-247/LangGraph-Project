from chatbot import chatbot
from langchain_core.messages import HumanMessage , SystemMessage
import streamlit as st
import uuid



#utility functions

def generate_thread_id():
    thread_id = uuid.uuid4()
    return str(thread_id)


#creating a session 

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

#add sidebar

st.sidebar.title("Langgraph Chatbot")

st.sidebar.button("New Chat")

st.sidebar.subheader("My conversations")

st.sidebar.button(st.session_state["thread_id"])    




for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.text(msg["content"])



user_input = st.chat_input("Type your message here...")


thread_id = st.session_state["thread_id"]

CONFIG = {'configurable': {'thread_id': thread_id}}

if user_input:
    st.session_state['messages'].append({'role': 'human', 'content': user_input})
    with st.chat_message("human"):
        st.text(user_input)

    with st.chat_message("assistant"):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk , metadata in chatbot.stream(
                {
                    'messages': [
                    SystemMessage(content="You are a helpful Customer Support Agent. Always introduce yourself as 'Muhammad Aamish - Customer Support Services'."),
                    HumanMessage(content=user_input)],
                    'thread_id': thread_id
                },
                config=CONFIG,
                stream_mode= 'messages'
            )
        )
        st.session_state['messages'].append({'role': 'assistant', 'content': ai_message})