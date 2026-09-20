# Multi-Agent Research Assistant

An AI-powered multi-agent research system built with CrewAI, Google Gemini, and web search.

The system uses multiple specialized AI agents that collaborate sequentially to research a topic, analyze evidence, fact-check claims, and generate a structured technical report.

---

## 🚀 Project Overview

The Multi-Agent Research Assistant automates the research workflow using four specialized AI agents.

Instead of asking a single AI model to perform the entire task, the system divides the workflow into specialized responsibilities.

### Agent Pipeline

Research → Analysis → Fact Check → Report

```text
                    Research Topic
                         │
                         ▼
              ┌─────────────────────┐
              │  Research Librarian │
              │     Web Search      │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │   Research Analyst  │
              │ Evidence Analysis   │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │    Fact Checker     │
              │ Verify Claims       │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │ Technical Writer    │
              │ Final Report        │
              └──────────┬──────────┘
                         │
                         ▼
                  Markdown Report
```

---

## 🖥️ Web UI

A Streamlit interface (`system-01-research-crew/app.py`) wraps the crew so you can run it from a browser instead of the command line: enter a topic, click **Run Research Crew**, and watch the report render live with a download button when it's done.

```bash
cd system-01-research-crew
streamlit run app.py
```

This opens at `http://localhost:8501`.

---

## ⚙️ Setup

1. Clone the repo and create a virtual environment:

   ```bash
   python -m venv venv
   source venv/Scripts/activate   # Windows (Git Bash)
   # or: venv\Scripts\activate    # Windows (cmd/PowerShell)
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and add your free Gemini API key from [Google AI Studio](https://aistudio.google.com/):

   ```
   GEMINI_API_KEY=your_key_here
   ```

4. Run it either from the command line:

   ```bash
   cd system-01-research-crew
   python main.py
   ```

   or via the Streamlit web UI (see above). Generated reports are saved as Markdown files in `reports/`.

---

## 🔧 Notes on this setup

This version fixes several issues found while getting the original code running:

- **Upgraded `crewai` from `0.83.0` to `1.15.22`.** The old version builds its tool-calling loop as a legacy text-based ReAct scratchpad, which appends a tool's result onto the model's own conversation turn instead of sending it back as a new "user" turn. Gemini's current API strictly requires conversations to end on a "user" turn, so almost every multi-step agent call failed with `Requests ending with a model turn are not supported`. The current `crewai` version uses Gemini's native tool-calling API instead, which avoids this entirely.
- **Pinned `litellm==1.102.0`** and dropped two unused dependencies (`langgraph`, `langchain-openai`) that were never imported anywhere in the code but were pinned to versions with conflicting `openai` SDK requirements, which made a clean install impossible.
- **Added the missing `google-genai` package** that `test_gemini.py` needs but that wasn't listed in `requirements.txt`.
- **Added the Streamlit web UI** described above.

**Free-tier rate limit:** Google's free Gemini API tier caps some models at 20 requests/day. A single crew run makes many calls (each agent can loop through several tool calls), so it's easy to hit that limit if you run the crew repeatedly in a day. `gemini-3.1-flash-lite` (the current default) has a separate quota bucket from the larger `gemini-3.6-flash` model. If you see a `429 RESOURCE_EXHAUSTED` error, you've hit the daily cap for that specific model — wait for it to reset, or switch `gemini_llm`'s model in `system-01-research-crew/agents.py` to a different one with unused quota.
