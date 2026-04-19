# ⚡ AgentFlow – Multi-Agent AI Automation Platform

> A production-grade multi-agent orchestration system built with LangGraph, Claude API, and FastAPI. Specialized agents for research, summarization, and code generation — all coordinated by an intelligent supervisor.

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.0.55-green)](https://langchain.com/langgraph)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-teal)](https://fastapi.tiangolo.com)
[![Claude](https://img.shields.io/badge/Claude-Anthropic-orange)](https://anthropic.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](https://docker.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📌 Overview

AgentFlow is a **multi-agent AI automation platform** that orchestrates specialized AI agents using **LangGraph**'s stateful graph architecture. A supervisor agent intelligently routes incoming tasks to the most appropriate specialist:

- 🔍 **Research Agent** — Web search via Tavily + synthesis
- 📝 **Summarizer Agent** — Structured summaries from long content
- 💻 **Code Agent** — Production-ready Python code generation

All exposed via a **FastAPI REST interface** with **Server-Sent Events (SSE)** for real-time streaming.

---

## ✨ Features

- 🤖 **Multi-Agent Orchestration** — LangGraph stateful graphs with conditional branching
- 🎯 **Intelligent Routing** — Supervisor node automatically routes to the right agent
- 🔍 **Tool Use** — Research agent has web search (Tavily) tool access
- 🌊 **Streaming** — Real-time SSE streaming of agent responses
- 🔄 **Human-in-the-Loop Ready** — Architecture supports checkpoint interrupts
- 🚀 **FastAPI REST** — Clean REST interface with auto Swagger docs
- 🐳 **Docker Ready** — Production containerized deployment

---

## 🏗️ Architecture

```
User Request
     │
     ▼
┌─────────────┐
│  SUPERVISOR  │  ← Analyzes task type
│    NODE      │
└──────┬───────┘
       │ Conditional Routing
       ▼                    ▼                    ▼
┌──────────┐    ┌────────────┐    ┌──────────────┐
│ RESEARCH │    │ SUMMARIZER │    │ CODE AGENT   │
│  AGENT   │    │   AGENT    │    │              │
└────┬─────┘    └─────┬──────┘    └──────┬───────┘
     │                │                  │
     ▼                ▼                  ▼
┌─────────┐         [END]              [END]
│  TOOLS  │
│  NODE   │
└────┬────┘
     │
    [END]
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Agent Orchestration | LangGraph |
| LLM | Claude 3 Haiku (Anthropic) |
| Web Search Tool | Tavily API |
| REST API | FastAPI |
| Streaming | Server-Sent Events (SSE) |
| Deployment | Docker + GCP Cloud Run |

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/prafulla2121/agentflow.git
cd agentflow
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add API Keys
```bash
cp .env.example .env
# Edit .env and add your keys
```

### 5. Run the API
```bash
uvicorn main:app --reload --port 8000
```

Open `http://localhost:8000/docs` for interactive Swagger UI.

---

## 📡 API Usage

### Run a task (auto-routed to best agent)
```bash
curl -X POST "http://localhost:8000/run" \
  -H "Content-Type: application/json" \
  -d '{"task": "Research the latest developments in LangGraph 2025"}'
```

### Stream response via SSE
```bash
curl -X POST "http://localhost:8000/run/stream" \
  -H "Content-Type: application/json" \
  -d '{"task": "Write a Python function to sort a list using quicksort"}'
```

### List available agents
```bash
curl http://localhost:8000/agents
```

---

## 🐳 Docker

```bash
docker build -t agentflow .
docker run -p 8000:8000 --env-file .env agentflow
```

---

## ☁️ GCP Cloud Run Deployment

```bash
# Build and push
gcloud builds submit --tag gcr.io/YOUR_PROJECT/agentflow

# Deploy
gcloud run deploy agentflow \
  --image gcr.io/YOUR_PROJECT/agentflow \
  --platform managed \
  --region YOUR_REGION \
  --allow-unauthenticated \
  --set-env-vars ANTHROPIC_API_KEY=your_key,OPENAI_API_KEY=your_key,TAVILY_API_KEY=your_key
```

---

## 📁 Project Structure

```
agentflow/
├── agents.py           # LangGraph multi-agent graph definition
├── main.py             # FastAPI app + SSE streaming endpoints
├── requirements.txt    # Dependencies
├── Dockerfile          # Container config
├── .env.example        # Environment template
├── .gitignore
└── README.md
```

---

## 🔮 Roadmap

- [ ] Human-in-the-loop checkpoint interrupts
- [ ] Persistent memory across sessions (Redis)
- [ ] Additional agents: Data Analyst, Email Writer
- [ ] LangSmith observability integration
- [ ] React frontend dashboard

---

## 📄 License

MIT License — see [LICENSE](LICENSE) file.

---

## 👤 Author

**Prafulla Purohit**  
🔗 [LinkedIn](https://linkedin.com/in/prafulla-purohit) | [GitHub](https://github.com/prafulla2121)
