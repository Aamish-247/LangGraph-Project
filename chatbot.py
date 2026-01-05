from langgraph.graph import StateGraph, START , END
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
load_dotenv()
from langgraph.checkpoint.memory import MemorySaver
from typing import Annotated, List
from pydantic import BaseModel
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import add_messages


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


checkpoint = MemorySaver()

#Define Graph

graph = StateGraph(chat_state)

graph.add_node('chat_bot' , chat_bot)

graph.add_edge(START , 'chat_bot')
graph.add_edge('chat_bot' , END)

chatbot = graph.compile(checkpointer=checkpoint)

