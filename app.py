from chatbot import chatbot
from langchain_core.messages import HumanMessage , SystemMessage
import streamlit as st

thread_id = '1'

CONFIG = {'configurable': {'thread_id': thread_id}}

st.title("Memory Based Chatbot")

#creating a session 

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.text(msg["content"])



user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state['messages'].append({'role': 'human', 'content': user_input})
    with st.chat_message("human"):
        st.text(user_input)

    response = chatbot.invoke(
        {
            'messages': [
                SystemMessage(
                    content="You are a helpful Customer Support Agent. Always introduce yourself as 'Muhammad Aamish - Customer Support Services'."
                ),
                HumanMessage(content=user_input)
            ]
        },
        config=CONFIG
    )
    ai_message = response['messages'][-1].content

    st.session_state['messages'].append({'role': 'assistant', 'content': ai_message})
    with st.chat_message("assistant"):
        st.text(ai_message)