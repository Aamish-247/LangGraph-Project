from langgraph.graph import StateGraph, START , END
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
load_dotenv()
from langgraph.checkpoint.sqlite import SqliteSaver
from typing import Annotated, List
from pydantic import BaseModel
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
import sqlite3
from langchain_core.messages import HumanMessage , SystemMessage


#define LLM

model  = ChatGroq(model = 'llama-3.3-70b-versatile' , api_key= os.getenv('GROQ_API_KEY'))


#define state
class chat_state(BaseModel):

    messages : Annotated[List[BaseMessage], add_messages] = []



#Define chat bot

def chat_bot(state: chat_state):

    messages = state.messages

    response = model.invoke(messages)

    return {'messages': [response]}

conn = sqlite3.connect(database="chat_history.db", check_same_thread=False)

memory = SqliteSaver(conn)

#Define Graph

graph = StateGraph(chat_state)

graph.add_node('chat_bot' , chat_bot)

graph.add_edge(START , 'chat_bot')
graph.add_edge('chat_bot' , END)

chatbot = graph.compile(checkpointer=memory)

CONFIG = {'configurable': {'thread_id': '1234'}}

Result = chatbot.invoke(
                {
                    'messages': [ HumanMessage(content= "my name is Umer and i am feeling hungry")]
                },
                config=CONFIG
            )

print(Result)