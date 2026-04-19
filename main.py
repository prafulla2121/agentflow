"""
AgentFlow – FastAPI REST Interface
Supports streaming responses via Server-Sent Events (SSE)
"""

import asyncio
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from agents import agent_graph

app = FastAPI(
    title="AgentFlow API",
    description="Multi-Agent AI Automation Platform powered by LangGraph + Claude",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class TaskRequest(BaseModel):
    task: str
    stream: bool = False


class TaskResponse(BaseModel):
    agent_used: str
    task_type: str
    output: str
    status: str


@app.get("/")
def root():
    return {
        "message": "AgentFlow Multi-Agent Platform is running!",
        "version": "1.0.0",
        "agents": ["supervisor", "research_agent", "summarizer", "code_agent"],
    }


@app.get("/health")
def health():
    return {"status": "healthy", "agents": "ready"}


@app.post("/run", response_model=TaskResponse)
def run_agent(request: TaskRequest):
    try:
        initial_state = {
            "messages": [HumanMessage(content=request.task)],
            "task_type": "",
            "current_agent": "supervisor",
            "final_output": "",
        }
        result = agent_graph.run(initial_state)
        return TaskResponse(
            agent_used=result.get("current_agent", "supervisor"),
            task_type=result.get("task_type", "research"),
            output=result.get("final_output", ""),
            status="success",
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/run/stream")
async def run_agent_stream(request: TaskRequest):
    async def generate():
        try:
            response = run_agent(request)
            payload = json.dumps(response.dict())
            yield f"data: {payload}\n\n"
        except Exception as exc:
            error_payload = json.dumps({"error": str(exc)})
            yield f"data: {error_payload}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


@app.get("/agents")
def list_agents():
    return {
        "agents": [
            {
                "name": "supervisor",
                "capabilities": "Routes tasks to the most appropriate specialist",
            },
            {
                "name": "research_agent",
                "capabilities": "Researches and summarizes web search results",
            },
            {
                "name": "summarizer",
                "capabilities": "Produces concise summaries of long content",
            },
            {
                "name": "code_agent",
                "capabilities": "Generates production-ready Python code",
            },
        ]
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
