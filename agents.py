from typing import Sequence, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_anthropic import ChatAnthropic
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.graph import StateGraph, END
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatAnthropic(
    model="claude-3-haiku-20240307",
    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
    temperature=0.3,
)

search_tool = TavilySearchResults(
    max_results=3,
    tavily_api_key=os.getenv("TAVILY_API_KEY"),
)


class AgentState(TypedDict):
    messages: Sequence[BaseMessage]
    task_type: str
    current_agent: str
    final_output: str


def supervisor_node(state: AgentState) -> AgentState:
    """Route tasks to the appropriate specialized agent."""
    messages = state.get("messages", [])
    last_message = messages[-1].content.lower() if messages else ""

    if any(k in last_message for k in ["code", "function", "script", "program", "python"]):
        task_type = "code"
    elif any(k in last_message for k in ["summarize", "summary", "brief", "tldr"]):
        task_type = "summarize"
    else:
        task_type = "research"

    return {**state, "task_type": task_type, "current_agent": "supervisor"}


def research_agent_node(state: AgentState) -> AgentState:
    """Research agent with web search capabilities."""
    messages = state.get("messages", [])
    prompt = messages[-1].content if messages else ""
    system_prompt = (
        "You are an expert research agent. Your job is to:\n"
        "1. Use the web search results below as your main source\n"
        "2. Synthesize findings into clear, cited responses\n"
        "3. Always mention your sources"
    )
    results = search_tool.invoke(prompt)

    response = llm.invoke(
        [HumanMessage(content=f"{system_prompt}\n\nSearch results:\n{results}\n\nTask: {prompt}")]
    )
    return {
        **state,
        "messages": [*messages, response],
        "current_agent": "research_agent",
        "final_output": response.content,
    }


def summarizer_agent_node(state: AgentState) -> AgentState:
    """Summarization agent for condensing content."""
    messages = state.get("messages", [])
    prompt = messages[-1].content if messages else ""
    system_prompt = (
        "You are an expert summarization agent. Your job is to:\n"
        "1. Extract the key points from provided content\n"
        "2. Create concise, structured summaries\n"
        "3. Use bullet points for clarity\n"
        "4. Highlight the most important insights"
    )

    response = llm.invoke([HumanMessage(content=system_prompt + "\n\nTask: " + prompt)])
    return {
        **state,
        "messages": [*messages, response],
        "current_agent": "summarizer",
        "final_output": response.content,
    }


def code_agent_node(state: AgentState) -> AgentState:
    """Code generation agent."""
    messages = state.get("messages", [])
    prompt = messages[-1].content if messages else ""
    system_prompt = (
        "You are an expert Python code generation agent. Your job is to:\n"
        "1. Write clean, well-commented, production-ready Python code\n"
        "2. Follow PEP 8 style guidelines\n"
        "3. Include docstrings and type hints\n"
        "4. Add usage examples in comments\n"
        "5. Handle edge cases and add error handling"
    )

    response = llm.invoke([HumanMessage(content=system_prompt + "\n\nTask: " + prompt)])
    return {
        **state,
        "messages": [*messages, response],
        "current_agent": "code_agent",
        "final_output": response.content,
    }


def route_after_supervisor(state: AgentState) -> str:
    """Route to the correct agent based on task type."""
    task_type = state.get("task_type", "research")
    if task_type == "code":
        return "code_agent"
    elif task_type == "summarize":
        return "summarizer"
    return "research_agent"


def build_agent_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("research_agent", research_agent_node)
    workflow.add_node("summarizer", summarizer_agent_node)
    workflow.add_node("code_agent", code_agent_node)

    workflow.set_entry_point("supervisor")

    workflow.add_conditional_edges("supervisor", route_after_supervisor)

    workflow.add_edge("research_agent", END)
    workflow.add_edge("summarizer", END)
    workflow.add_edge("code_agent", END)

    return workflow.compile()


agent_graph = build_agent_graph()
