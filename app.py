from chatbot import chatbot
from langchain_core.messages import HumanMessage , SystemMessage
import streamlit as st
import uuid

#creating a session 

if 'messages' not in st.session_state:
    st.session_state['messages'] = [] 

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = []

#utility functions

def generate_thread_id():
    thread_id = uuid.uuid4()
    return str(thread_id)

def reset_chat():
    st.session_state["messages"] = []
    st.session_state["thread_id"] = generate_thread_id()
    add_thread(st.session_state["thread_id"])



def add_thread(thread_id):
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)    

def get_chat_history(thread_id):
    state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})     
    return state.values.get('messages', [])   


if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()


add_thread(st.session_state["thread_id"])   

#add sidebar

st.sidebar.title("Langgraph Chatbot")

if st.sidebar.button("New Chat"):
    reset_chat()  

st.sidebar.subheader("My conversations")

for thread_id in st.session_state["chat_threads"][::-1]:

    if st.sidebar.button(str(thread_id)):
        st.session_state["thread_id"] = thread_id
        messages = get_chat_history(thread_id)

        temp_messages = []
        for msg in messages:
            
            if isinstance(msg, SystemMessage):
                continue

            if isinstance(msg, HumanMessage):
                role = "user"

            else:
                role = "assistant"

            temp_messages.append({
                'role': role,
                'content': msg.content
            })

        st.session_state["messages"] = temp_messages
       
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.text(msg["content"])



user_input = st.chat_input("Type your message here...")


thread_id = st.session_state["thread_id"]

CONFIG = {'configurable': {'thread_id': thread_id}}

if user_input:
    st.session_state['messages'].append({'role': 'user', 'content': user_input})
    with st.chat_message("user"):
        st.text(user_input)

    with st.chat_message("assistant"):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk in chatbot.stream(
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