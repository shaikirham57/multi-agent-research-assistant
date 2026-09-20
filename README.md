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

This version pins `litellm==1.102.0` and drops two unused dependencies (`langgraph`, `langchain-openai`) that were never imported anywhere in the code but were pinned to versions with conflicting `openai` SDK requirements, which made a clean install impossible. It also adds the `google-genai` package that `test_gemini.py` needs but that was missing from `requirements.txt`, and the Streamlit web UI described above.
