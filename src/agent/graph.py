from pathlib import Path

from dotenv import load_dotenv
from langchain_core.messages import SystemMessage
from langchain_groq import ChatGroq

from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import InMemorySaver

from src.agent.prompts import SYSTEM_PROMPT
from src.tools.product_tools import search_products
from src.tools.order_tools import get_order_status
from src.tools.policy_tools import search_store_policies

load_dotenv() 

tools = [
    search_products,
    get_order_status,
    search_store_policies
]

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=2
)

llm_with_tools = llm.bind_tools(tools)

def call_agent(state: MessagesState):
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        *state["messages"]
    ]
    
    response = llm_with_tools.invoke(messages)
    
    return {"messages": [response]}


builder = StateGraph(MessagesState)

builder.add_node("agent", call_agent)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "agent")

builder.add_conditional_edges(
    "agent",
    tools_condition
)

builder.add_edge("tools", "agent")

memory = InMemorySaver()

agent = builder.compile(checkpointer=memory)