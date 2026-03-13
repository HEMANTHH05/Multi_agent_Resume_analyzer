# Multi-Agent Resume Analyzer

A demo project built to explore and analyze **agentic workflows** using the Claude API. Instead of sending everything to a single LLM call (which leads to hallucinations and missed rules), this project breaks the resume tailoring process into **9 specialized agents** — each doing one job, cross-checking rules, and passing structured output to the next.

---

## What This Demonstrates

This project is a practical case study in agentic design patterns:

| Pattern | Where It Appears |
|---|---|
| **Sequential agent pipeline** | 9 agents run in order, each building on the last |
| **Structured context passing** | Every agent's output feeds into a shared `pipeline_context` dict |
| **Human-in-the-loop (HITL)** | Pipeline pauses mid-run and asks the user for input when ambiguity is detected |
| **Streaming output** | Each agent streams its Claude response token-by-token to the UI in real time |
| **Validation gate** | A dedicated validator agent cross-checks every other agent's output before finalizing |
| **Selective context injection** | Each agent only receives the context it needs — not the full history |

---

## Agent Pipeline

```
Resume (PDF/DOCX) + Job Description
           │
           ▼
  ┌─────────────────┐
  │  1. ParseAgent  │  Extracts text from PDF/DOCX — no Claude, pure Python
  └────────┬────────┘
           ▼
  ┌──────────────────────┐
  │  2. MatchScorerAgent │  Overall match score + 6-category breakdown (0–100%)
  └────────┬─────────────┘
           ▼
  ┌──────────────────────────┐
  │  3. KeywordExtractorAgent│  Every missing/misaligned JD keyword flagged 🔴🟡
  └────────┬─────────────────┘
           ▼
  ┌────────────────────┐
  │  4. RoleSafetyAgent│  Detects significant role shifts → PAUSES for user input
  └────────┬───────────┘
           ▼
  ┌─────────────────────┐
  │  5. DomainMapperAgent│  Maps each client/project to its industry domain
  └────────┬────────────┘     → PAUSES if any domain is ambiguous
           ▼
  ┌──────────────────────────┐
  │  6. NarrativeBuilderAgent│  Plans skill threading across career stages
  └────────┬─────────────────┘
           ▼
  ┌────────────────────────┐
  │  7. ResumeRewriterAgent │  Full project-by-project rewrite with 4-check
  └────────┬───────────────┘   validation gate + bullet count enforcement
           ▼
  ┌─────────────────┐
  │  8. ValidatorAgent│  Cross-checks ALL rules, finds issues, auto-fixes them
  └────────┬─────────┘
           ▼
  ┌──────────────────────────┐
  │  9. DocumentGeneratorAgent│  Generates final ATS-friendly .docx — no Claude
  └──────────────────────────┘
           │
           ▼
     Download Resume
```

---

## Architecture

```
Browser (React + Vite)
    │
    │  POST /upload       — resume file upload
    │  WS   /ws/{id}      — real-time pipeline communication
    │  GET  /download/{id} — fetch generated .docx
    ▼
FastAPI Backend
    │
    ▼
Orchestrator
  ├── pipeline_context dict  (grows as each agent completes)
  ├── asyncio.Event          (pause / resume for HITL)
  └── Sequential agent loop
        └── Each agent:
              ├── Reads from context (only what it needs)
              ├── Calls Claude API with streaming
              ├── Streams chunks → WebSocket → UI
              ├── Extracts structured JSON from response
              └── Writes output back to context
```

### Human-in-the-Loop Flow

```
Agent detects ambiguity
    → raises HumanInputRequired(prompt)
    → Orchestrator sends AGENT_PAUSED over WebSocket
    → UI activates chat bar with yellow banner
    → User types reply → USER_REPLY message sent
    → Orchestrator injects reply into agent
    → Agent resumes from checkpoint (no re-calling Claude)
    → Pipeline continues
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, TypeScript, Vite — plain CSS, no UI library |
| Backend | Python, FastAPI, WebSockets |
| AI | Anthropic Claude API (`claude-sonnet-4-6`), streaming |
| Resume parsing | `pdfplumber` (PDF), `python-docx` (DOCX) |
| Document output | `python-docx` |
| Real-time | WebSocket (bidirectional — streaming + HITL replies) |

---

## Project Structure

```
├── start.sh                        # Start both servers
├── resume_plan.md                  # Source rules for all agent prompts
├── backend/
│   ├── main.py                     # FastAPI: upload, WebSocket, download
│   ├── orchestrator.py             # Pipeline controller + pause/resume
│   ├── requirements.txt
│   ├── .env.example                # Copy to .env and add your API key
│   └── agents/
│       ├── base_agent.py           # Shared: streaming, Claude calls, HITL
│       ├── parse_agent.py
│       ├── match_scorer_agent.py
│       ├── keyword_extractor_agent.py
│       ├── role_safety_agent.py
│       ├── domain_mapper_agent.py
│       ├── narrative_builder_agent.py
│       ├── resume_rewriter_agent.py
│       ├── validator_agent.py
│       └── document_generator_agent.py
└── frontend/
    └── src/
        ├── App.tsx
        ├── hooks/useWebSocket.ts   # Full WebSocket protocol handler
        ├── types/index.ts
        └── components/
            ├── TopBar.tsx          # 9-step progress indicator
            ├── UploadPanel.tsx     # Drag & drop resume upload
            ├── JDPanel.tsx         # Job description input
            ├── AgentFeed.tsx       # Streaming agent output feed
            ├── ChatBar.tsx         # HITL reply input
            ├── MatchScoreCard.tsx  # Visual score ring + bars
            └── KeywordList.tsx     # 🔴🟡 keyword gap grid
```

---

## WebSocket Message Protocol

All real-time communication between backend and frontend uses typed JSON messages over a single WebSocket connection.

**Server → Client**
```json
{ "type": "PIPELINE_STARTED", "steps": ["ParseAgent", "MatchScorerAgent", ...] }
{ "type": "AGENT_STARTED",    "agent": "MatchScorerAgent", "step_index": 1 }
{ "type": "AGENT_CHUNK",      "agent": "MatchScorerAgent", "text": "Based on..." }
{ "type": "STRUCTURED_OUTPUT","agent": "MatchScorerAgent", "key": "match_score", "data": {...} }
{ "type": "AGENT_PAUSED",     "agent": "RoleSafetyAgent",  "prompt": "Role shift detected..." }
{ "type": "AGENT_RESUMED",    "agent": "RoleSafetyAgent" }
{ "type": "AGENT_COMPLETE",   "agent": "MatchScorerAgent", "step_index": 1 }
{ "type": "DOWNLOAD_READY",   "url": "/download/abc123" }
{ "type": "PIPELINE_COMPLETE" }
```

**Client → Server**
```json
{ "type": "START",       "jd_text": "..." }
{ "type": "USER_REPLY",  "text": "Option 2 — ML-first pivot" }
```

---

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- An [Anthropic API key](https://console.anthropic.com)

### Setup

```bash
# Clone
git clone https://github.com/HEMANTHH05/Multi_agent_Resume_analyzer.git
cd Multi_agent_Resume_analyzer

# Backend
cd backend
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Add your Anthropic API key to .env

# Frontend
cd ../frontend
npm install
```

### Run

```bash
# From project root
./start.sh
```

Then open **http://localhost:5173**

---

## How to Use

1. **Drop your resume** (PDF or DOCX) on the left panel
2. **Paste the full job description** on the right panel
3. Click **Start Analysis →**
4. Watch each agent stream its analysis in real time
5. If a **role shift** or **ambiguous client domain** is detected → the chat bar activates — type your answer and press Enter to resume
6. When all 9 agents complete → click **Download Resume (.docx)**

---

## Key Design Decisions

**Why sequential agents instead of one big prompt?**
Single large prompts tend to skip rules, hallucinate keywords, and ignore validation constraints. Breaking the work into focused agents with narrow system prompts produces more reliable, rule-adherent output at each step.

**Why WebSockets instead of HTTP polling?**
The pipeline needs to be bidirectional — streaming tokens from the server *and* receiving user replies mid-run. WebSocket handles both in one persistent connection cleanly.

**Why in-memory state instead of a database?**
This is a single-session, start-to-finish local tool. The full pipeline runs in one sitting. In-memory context is simpler, faster, and has no setup overhead. A database would only be needed for multi-user or persistent session history.

---

## License

MIT
