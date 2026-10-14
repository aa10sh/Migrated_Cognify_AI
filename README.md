#  Cognify AI — React & LangGraph Edition

> An Agentic AI-powered cognitive recall and memory benchmark application.

Cognify AI evaluates how well a user can **read, comprehend, retain, and accurately reproduce** technical information under time constraints. Instead of relying on a single naive similarity score, it evaluates recall across multiple independent dimensions using **LangGraph parallel multi-agent orchestration** and modern NLP techniques.

<p align="center">
  <img src="assets/banner.png" alt="Cognify AI Banner" width="85%"/>
</p>

---

## 📑 Table of Contents

1. [Overview](#-overview)
2. [Key Features](#-key-features)
3. [What's New in the React Edition](#-whats-new-in-the-react-edition)
4. [Core Workflow](#-core-workflow)
5. [Evaluation System](#-evaluation-system)
6. [LangGraph Architecture](#-langgraph-architecture)
7. [System Architecture](#-system-architecture)
8. [Technology Stack](#-technology-stack)
9. [Project Structure](#-project-structure)
10. [Frontend Details](#-frontend-details)
11. [Backend Details](#-backend-details)
12. [API Reference](#-api-reference)
13. [Quick Start](#-quick-start)
14. [Development Mode](#-development-mode)
15. [Configuration](#-configuration)
16. [Screenshots](#-screenshots)
17. [Troubleshooting](#-troubleshooting)
18. [Future Plans](#-future-plans)
19. [Author](#-author)

---

## 📖 Overview

The user picks a topic, word count, difficulty, and reading/recall timers. Cognify then generates a validated reading passage, shows it for a limited time, hides it completely, and asks the user to write down everything they remember.

The recall is analysed by **four independent evaluation agents** running in parallel. Their outputs are synthesized by a **Final Evaluator** into:

- An overall performance score (**0–100**)
- A performance level / badge
- A strengths breakdown
- A list of missed concepts
- Actionable, personalized AI feedback

---

## ✨ Key Features

- **Multi-dimensional recall scoring** — semantic, coverage, faithfulness, and language quality evaluated separately.
- **LangGraph orchestration** — one graph for content generation (with a validation/regeneration loop) and one for parallel evaluation.
- **Validated content generation** — Pydantic schemas and target word-count bounds guarantee well-formed challenges.
- **Timed Reading & Recall phases** — synchronized countdown timers; passage disappears completely after reading.
- **Auto-submit** — recall is submitted manually or automatically when the timer expires.
- **Live writing stats** — real-time word count while recalling.
- **Resilient multi-mode engine** — runs fully offline with local Hugging Face models; OpenAI is used optionally for passage generation and feedback synthesis.
- **Modern React UI** — responsive, animated, with a score meter, performance badge, and deep-dive inspector.
- **Single-command deployment** — one command starts the API and serves the compiled React app.

---

## 🚀 What's New in the React Edition

| Area | Previous (Streamlit) | Now (React Edition) |
|---|---|---|
| Frontend | Streamlit (`app.py`) | React 19 + Vite + Tailwind CSS |
| Backend | Called directly from Streamlit | FastAPI REST API (`server.py`) |
| Icons / Effects | Basic Streamlit widgets | Lucide icons, canvas-confetti |
| Settings | `.env` only | `.env` **or** in-app Settings modal |
| Deployment | `streamlit run app.py` | `python run.py` / `run.bat` |
| Evaluation graph | Language node after the other three | All four nodes execute in parallel |

> The **core application logic, agents, graphs, and NLP modules are unchanged** — only the frontend was migrated and a REST layer was added.

---

## 🔄 Core Workflow

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

### Phase-by-phase

1. **Setup** — Choose topic, word limit, difficulty, reading time, and recall time.
2. **Content Generation** — The Content Generation Graph generates a passage, extracts key concepts, validates the result, and regenerates if validation fails.
3. **Reading** — The passage is shown with a countdown timer.
4. **Recall** — The passage is hidden; the user writes what they remember. Submission is manual or automatic on timer expiry.
5. **Evaluation** — The Evaluation Graph runs the four agents in parallel, then the Final Evaluator.
6. **Results** — Score dashboard with tabs and a deep-dive inspector.

---

## 🧪 Evaluation System

| Evaluation | Purpose | Technique / Model |
|---|---|---|
| **Semantic Similarity** | Measures similarity in overall meaning | SentenceTransformer embeddings + cosine similarity — `sentence-transformers/all-MiniLM-L6-v2` |
| **Concept Coverage** | Measures how many important concepts were remembered; lists covered & missed concepts | Key-concept matching with similarity thresholds |
| **Faithfulness** | Checks whether recalled claims are supported by the original passage | Source-sentence retrieval + NLI — `cross-encoder/nli-MiniLM2-L6-H768` |
| **Language Coherence** | Evaluates grammar, clarity, coherence, and organization | Linguistic rubric |

### Final Score Weighting

| Dimension | Weight |
|---|---|
| Semantic Similarity | **25%** |
| Concept Coverage | **35%** |
| Faithfulness | **25%** |
| Language Coherence | **15%** |

```text
Final Score = 0.25·Semantic + 0.35·Coverage + 0.25·Faithfulness + 0.15·Language
```

### Faithfulness details

For every statement in the user's recall, the system:

1. Finds the **most relevant sentence** in the original passage.
2. Runs an **NLI cross-encoder** on the (source, claim) pair.
3. Classifies it as **Entailment**, **Neutral**, or **Contradiction**.

---

## 🕸️ LangGraph Architecture

Cognify uses **two separate LangGraph workflows**.

### 1. Content Generation Graph

```text
START
  ↓
Generate Challenge
  ↓
Validate Challenge
  ↓
 ┌───────────────┐
 │               │
Valid          Invalid
 │               │
 ↓               ↓
END         Regenerate
                │
                └──→ Validate
```

<p align="center">
  <img src="assets/content_graph.png" alt="Content Generation Graph" width="60%"/>
  <br/>
  <em>Content Generation Graph — generation ↔ validation loop</em>
</p>

### 2. Evaluation Graph (Parallel)

```text
                    START
                      │
   ┌──────────┬───────┴───────┬──────────────┐
   ↓          ↓               ↓              ↓
Semantic   Coverage      Faithfulness   Language Coherence
   │          │               │              │
   └──────────┴───────┬───────┴──────────────┘
                      ↓
              Final Evaluator
                      ↓
                     END
```

<p align="center">
  <img src="assets/evaluation_graph.png" alt="Evaluation Graph" width="60%"/>
  <br/>
  <em>Evaluation Graph — four parallel agents feeding the Final Evaluator</em>
</p>

---

## 🏗️ System Architecture

```text
┌────────────────────────┐        HTTP / JSON        ┌──────────────────────────────┐
│  React Frontend (Vite) │ ◄───────────────────────► │      FastAPI (server.py)     │
│  Tailwind · Lucide     │   /api/* (proxied in dev) │                              │
└────────────────────────┘                           │  ┌────────────────────────┐  │
                                                     │  │  Content Graph         │  │
                                                     │  │  (LangGraph)           │  │
                                                     │  └────────────────────────┘  │
                                                     │  ┌────────────────────────┐  │
                                                     │  │  Evaluation Graph      │  │
                                                     │  │  (LangGraph, parallel) │  │
                                                     │  └────────────────────────┘  │
                                                     │  ┌──────────┐ ┌───────────┐  │
                                                     │  │ NLP      │ │ LLM client│  │
                                                     │  │ (HF)     │ │ (OpenAI / │  │
                                                     │  │          │ │ offline)  │  │
                                                     │  └──────────┘ └───────────┘  │
                                                     └──────────────────────────────┘
```

<p align="center">
  <img src="assets/architecture.png" alt="System Architecture" width="75%"/>
</p>

In production mode, FastAPI also **serves the compiled React build** as static files, so a single process on `http://localhost:8000` provides both UI and API.

---

## 🧰 Technology Stack

**Frontend**

- React 19
- Vite
- Tailwind CSS
- Lucide React (icons)
- canvas-confetti

**Backend**

- Python 3.11+
- FastAPI + Uvicorn
- LangGraph
- Pydantic

**AI / NLP**

- Sentence Transformers (`all-MiniLM-L6-v2`)
- Cross-Encoder NLI (`nli-MiniLM2-L6-H768`)
- PyTorch
- Hugging Face
- OpenAI API (optional — default model `gpt-4o-mini`)

---

## 📁 Project Structure

```text
ModifiedCognifyAI/
├── frontend/                       # React Frontend (Vite + Tailwind CSS)
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx          # Navigation & system status
│   │   │   ├── Sidebar.jsx         # Phase stepper & parameters card
│   │   │   ├── SetupPhase.jsx      # Challenge configuration form
│   │   │   ├── ReadingPhase.jsx    # Countdown timer & passage display
│   │   │   ├── RecallPhase.jsx     # Timed recall writing area
│   │   │   ├── EvaluationPhase.jsx # LangGraph parallel execution visualizer
│   │   │   ├── ResultPhase.jsx     # Multi-agent score dashboard & tabs
│   │   │   └── SettingsModal.jsx   # OpenAI API key & model settings
│   │   ├── App.jsx                 # Master React state controller
│   │   ├── index.css               # Tailwind base styles
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js              # Vite config with backend proxy
│
├── agents/                         # LangGraph Agent Nodes
│   ├── content_agent.py            # Generates reading passage & key concepts
│   ├── content_validator_agent.py  # Validates passage word count & coherence
│   ├── semantic_agent.py           # Evaluates semantic similarity
│   ├── coverage_agent.py           # Evaluates key concept coverage
│   ├── faithfulness_agent.py       # NLI entailment & contradiction check
│   ├── language_coherence_agent.py # Writing quality & grammar rubric
│   └── final_evaluator_agent.py    # Synthesizes final weighted score
│
├── graph/                          # StateGraph Workflows
│   ├── content_graph.py            # Generation-validation loop graph
│   └── evaluation_graph.py         # Parallel multi-agent evaluation graph
│
├── nlp/                            # Core NLP & ML Modules
│   ├── embeddings.py               # SentenceTransformer embedding generator
│   ├── similarity.py               # Cosine similarity calculations
│   ├── coverage.py                 # Key concept threshold matcher
│   ├── nli.py                      # CrossEncoder NLI inference
│   └── faithfulness.py             # Sentence extraction & support verification
│
├── models/
│   ├── challenge.py                # Challenge Pydantic schema
│   └── llm.py                      # Resilient LLM client (OpenAI + offline fallback)
│
├── assets/                         # README images (graphs, screenshots)
│
├── server.py                       # FastAPI REST API & static file server
├── run.py                          # Unified launch script
├── run.bat                         # One-click Windows launcher
├── config.py                       # Challenge constants & word limits
├── requirements.txt                # Python dependencies
└── .env                            # (Optional) OpenAI credentials
```

---

## 🎨 Frontend Details

The frontend lives in `frontend/` and is a single-page React app. `App.jsx` is the **master state controller** that drives the phase flow: `setup → reading → recall → evaluation → result`.

| Component | Responsibility |
|---|---|
| `Navbar.jsx` | Top navigation bar and system/AI status indicator |
| `Sidebar.jsx` | Phase stepper showing progress, plus a card of current challenge parameters |
| `SetupPhase.jsx` | Form for topic, word count, difficulty, reading time, and recall time |
| `ReadingPhase.jsx` | Displays the generated passage with a synchronized countdown timer |
| `RecallPhase.jsx` | Timed writing area with live word count and stats; auto-submits at 0:00 |
| `EvaluationPhase.jsx` | Visualizes the LangGraph parallel execution while the evaluation runs |
| `ResultPhase.jsx` | Score meter, performance badge, strengths, missed concepts, tabbed deep-dive inspector, confetti on high scores |
| `SettingsModal.jsx` | Enter/update OpenAI API key and model without editing `.env` |

**Dev proxy:** `vite.config.js` proxies `/api/*` requests to `http://localhost:8000`, so the dev server on port `3000` talks to the FastAPI backend seamlessly.

---

## ⚙️ Backend Details

### `server.py` — FastAPI application

- Exposes the REST endpoints listed in the [API Reference](#-api-reference).
- Invokes the **Content Graph** and **Evaluation Graph**.
- Serves the compiled React build (`frontend/dist`) as static files.

### Agents (`agents/`)

| Agent | Role |
|---|---|
| `content_agent.py` | Generates the passage and extracts key concepts |
| `content_validator_agent.py` | Validates word-count bounds and coherence; triggers regeneration if invalid |
| `semantic_agent.py` | Embedding-based similarity score |
| `coverage_agent.py` | Covered / missed concept analysis |
| `faithfulness_agent.py` | NLI-based entailment / neutral / contradiction check |
| `language_coherence_agent.py` | Grammar, clarity, coherence, organization rubric |
| `final_evaluator_agent.py` | Weighted synthesis, performance level, and feedback |

### Graphs (`graph/`)

- `content_graph.py` — Generate → Validate → (Regenerate loop) → END.
- `evaluation_graph.py` — START → four parallel nodes → Final Evaluator → END.

### NLP modules (`nlp/`)

- `embeddings.py` — Loads `all-MiniLM-L6-v2` and produces embeddings.
- `similarity.py` — Cosine similarity utilities.
- `coverage.py` — Threshold-based concept matcher.
- `nli.py` — CrossEncoder NLI inference.
- `faithfulness.py` — Sentence extraction and support verification.

### Models (`models/`)

- `challenge.py` — Pydantic schema for a challenge (topic, passage, key concepts, limits).
- `llm.py` — **Resilient LLM client**: uses OpenAI when a key is available and automatically falls back to offline mode otherwise.

### Resilient Multi-Mode Engine

| Mode | Passage Generation | Feedback | NLP Scoring |
|---|---|---|---|
| **With OpenAI key** | OpenAI (`gpt-4o-mini` by default) | OpenAI-synthesized | Local HF models |
| **Offline / no key** | Local fallback | Local fallback | Local HF models |

---

## 🔌 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Health check endpoint |
| `GET` | `/api/config` | Retrieves challenge options and AI status |
| `POST` | `/api/settings` | Updates OpenAI API key & model settings |
| `POST` | `/api/challenge/generate` | Generates a validated reading challenge |
| `POST` | `/api/challenge/evaluate` | Executes the LangGraph parallel evaluation |

Interactive API docs (FastAPI default) are available at `http://localhost:8000/docs` when the server is running.

---

## ⚡ Quick Start

### 1. Prerequisites

- Python **3.11+**
- Node.js **v18+** and npm

### 2. Clone the repository

```bash
git clone <repository-url>
cd ModifiedCognifyAI
```

### 3. Backend environment setup

```powershell
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

*(macOS / Linux)*

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. *(Optional)* Configure OpenAI

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

You can also set the key later from the **Settings modal** inside the app.

### 5. Launch the application

```powershell
python run.py
```

Or double-click **`run.bat`** in Windows Explorer.

The script starts the FastAPI + LangGraph server and opens the React app at:

👉 **http://localhost:8000**

> **First run:** the Hugging Face models (`all-MiniLM-L6-v2`, `nli-MiniLM2-L6-H768`) are downloaded and cached, so the first evaluation may take a little longer.

---

## 🛠️ Development Mode

Run frontend and backend separately with hot module reloading.

**1. Start the FastAPI backend**

```powershell
python -m uvicorn server:app --reload --port 8000
```

**2. Start the Vite React dev server**

```powershell
cd frontend
npm install
npm run dev
```

Open **http://localhost:3000** — API requests are automatically proxied to port `8000`.

**Build the frontend for production**

```powershell
cd frontend
npm run build
```

The compiled output is then served by FastAPI at `http://localhost:8000`.

---

## 🔧 Configuration

| Setting | Location | Description |
|---|---|---|
| `OPENAI_API_KEY` | `.env` or Settings modal | Enables OpenAI passage generation and feedback |
| `OPENAI_MODEL` | `.env` or Settings modal | OpenAI model name (default `gpt-4o-mini`) |
| Challenge constants & word limits | `config.py` | Topic options, difficulty levels, min/max word bounds, timer ranges |
| Dev proxy | `frontend/vite.config.js` | Backend proxy target for the Vite dev server |
| Score weights | `agents/final_evaluator_agent.py` | 25% Semantic · 35% Coverage · 25% Faithfulness · 15% Language |

---

## 🖼️ Screenshots

| Setup | Reading |
|---|---|
| ![Setup Phase](assets/setup.png) | ![Reading Phase](assets/reading.png) |

| Recall | Evaluation |
|---|---|
| ![Recall Phase](assets/recall.png) | ![Evaluation Phase](assets/evaluation.png) |

| Results Dashboard | Deep-Dive Inspector |
|---|---|
| ![Result Phase](assets/result.png) | ![Deep Dive](assets/deep_dive.png) |

---

## 🩺 Troubleshooting

| Problem | Solution |
|---|---|
| `Port 8000 already in use` | Stop the other process or change the port in `run.py` / the uvicorn command |
| Blank page at `localhost:8000` | The frontend is not built — run `npm run build` inside `frontend/` |
| API errors in dev mode | Make sure the backend is running on port `8000` before starting Vite |
| Slow first evaluation | Models are being downloaded/cached from Hugging Face — subsequent runs are faster |
| OpenAI errors | Verify the API key in `.env` or Settings; the app falls back to offline mode when unavailable |
| `venv` activation blocked (PowerShell) | Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |

---

## 🔮 Future Plans

- Database integration
- User accounts and progress tracking
- Adaptive difficulty based on previous performance
- Asynchronous and distributed evaluation
- Dedicated ML inference services
- Docker and AWS deployment
- CI/CD pipeline
- Logging and monitoring

The long-term goal is to evolve Cognify into a **personalized cognitive training platform** that adapts challenges to the user's previous performance.

---

## 👤 Author

**Adarsh Singh**
