# Cognify AI — React & LangGraph Edition

Cognify AI is an Agentic AI-powered cognitive recall and memory benchmark application. It evaluates how well a user can read, comprehend, retain, and accurately reproduce technical information under time constraints.

Instead of relying on a single naive score, Cognify evaluates recall across multiple independent dimensions using **LangGraph parallel multi-agent orchestration** and NLP techniques:

- **Semantic Understanding** (SentenceTransformer vector embeddings & cosine similarity)
- **Concept Coverage** (Key concept matching & coverage percentage)
- **Faithfulness & Accuracy** (Cross-Encoder NLI entailment and contradiction detection)
- **Language & Coherence** (Grammar, clarity, coherence, and structural organization)

The independent agent evaluations are synthesized into an overall performance score (0–100), performance level, strengths breakdown, missed concepts, and actionable AI feedback.

---

## 🚀 Key Improvements & Architecture

- **React Frontend**: Replaced Streamlit with a modern, responsive React 19 application powered by Vite, Tailwind CSS, Lucide icons, and canvas-confetti.
- **FastAPI Backend**: High-performance RESTful API exposing challenge generation and LangGraph evaluation.
- **Resilient Multi-Mode Engine**: Operates out-of-the-box using local Hugging Face NLP models (`all-MiniLM-L6-v2` and `nli-MiniLM2-L6-H768`), with dynamic OpenAI integration for passage generation and feedback synthesis.
- **Unified Full-Stack Deployment**: A single command runs both the backend and serves the compiled React application at `http://localhost:8000`.

---

## 🧠 Core Workflow

```text
Setup Phase (Topic, Word Count, Difficulty, Reading & Recall Timers)
  ↓
Content Generation Agent + Validation (Pydantic & Target Word Bounds)
  ↓
Reading Phase (Passage view with synchronized countdown timer)
  ↓
Passage Disappears Completely
  ↓
Recall Phase (Timed writing space with live word count & stats)
  ↓
LangGraph Evaluation Graph (Parallel Orchestration)
  ├── 1. Semantic Similarity Node (all-MiniLM-L6-v2)
  ├── 2. Concept Coverage Node (Threshold matching)
  ├── 3. Faithfulness Node (cross-encoder/nli-MiniLM2-L6-H768)
  └── 4. Language Coherence Node (Linguistic rubric)
          ↓
  5. Final Evaluator Node (Weighted synthesis: 25% Sem, 35% Cov, 25% Faith, 15% Lang)
          ↓
Result Phase (Score meter, performance badge, strengths, missed concepts, deep-dive inspector)
```

---

## 📁 Project Structure

```text
ModifiedCognifyAI/
├── frontend/                     # React Frontend (Vite + Tailwind CSS)
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx        # Navigation & system status
│   │   │   ├── Sidebar.jsx       # Phase stepper & parameters card
│   │   │   ├── SetupPhase.jsx    # Challenge configuration form
│   │   │   ├── ReadingPhase.jsx  # Countdown timer & passage display
│   │   │   ├── RecallPhase.jsx   # Timed recall writing area
│   │   │   ├── EvaluationPhase.jsx # LangGraph parallel execution visualizer
│   │   │   ├── ResultPhase.jsx   # Multi-agent score dashboard & tabs
│   │   │   └── SettingsModal.jsx # OpenAI API key & model settings
│   │   ├── App.jsx               # Master React state controller
│   │   ├── index.css             # Tailwind base styles
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js            # Vite config with backend proxy
│
├── agents/                       # LangGraph Agent Nodes
│   ├── content_agent.py          # Generates reading passage & key concepts
│   ├── content_validator_agent.py# Validates passage word count & coherence
│   ├── semantic_agent.py         # Evaluates semantic similarity
│   ├── coverage_agent.py         # Evaluates key concept coverage
│   ├── faithfulness_agent.py     # NLI entailment & contradiction check
│   ├── language_coherence_agent.py # Writing quality & grammar rubric
│   └── final_evaluator_agent.py  # Synthesizes final weighted score
│
├── graph/                        # StateGraph Workflows
│   ├── content_graph.py          # Generation-validation loop graph
│   └── evaluation_graph.py       # Parallel multi-agent evaluation graph
│
├── nlp/                          # Core NLP & ML Modules
│   ├── embeddings.py             # SentenceTransformer embedding generator
│   ├── similarity.py             # Cosine similarity calculations
│   ├── coverage.py               # Key concept threshold matcher
│   ├── nli.py                    # CrossEncoder NLI inference
│   └── faithfulness.py           # Sentence extraction & support verification
│
├── models/
│   ├── challenge.py              # Challenge Pydantic schema
│   └── llm.py                    # Resilient LLM client (OpenAI + offline fallback)
│
├── server.py                     # FastAPI REST API & static file server
├── run.py                        # Unified launch script
├── run.bat                       # One-click Windows launcher
├── config.py                     # Challenge constants & word limits
└── requirements.txt              # Python dependencies
```

---

## ⚡ Quick Start

### 1. Prerequisites

- Python 3.11+
- Node.js v18+ & npm

### 2. Environment Setup

Create and activate a virtual environment:

```powershell
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

*(Optional)* Configure your OpenAI API key in `.env` (or configure it directly in the React UI via the Settings modal):

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

### 3. Launch the Application

Run the unified launch script:

```powershell
python run.py
```

Or double-click `run.bat` in Windows Explorer.

The application will automatically start the FastAPI + LangGraph server and open the React application in your browser at:
👉 **`http://localhost:8000`**

---

## 🛠️ Development Mode

To run frontend and backend with hot module reloading:

1. **Start the FastAPI backend:**
   ```powershell
   python -m uvicorn server:app --reload --port 8000
   ```

2. **Start the Vite React dev server:**
   ```powershell
   cd frontend
   npm run dev
   ```
   Open `http://localhost:3000` (API requests are automatically proxied to port 8000).

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Health check endpoint |
| `GET` | `/api/config` | Retrieves challenge options and AI status |
| `POST` | `/api/settings` | Updates OpenAI API key & model settings |
| `POST` | `/api/challenge/generate` | Generates a validated reading challenge |
| `POST` | `/api/challenge/evaluate` | Executes the LangGraph parallel evaluation |

---

## 👤 Author

**Adarsh Singh**
