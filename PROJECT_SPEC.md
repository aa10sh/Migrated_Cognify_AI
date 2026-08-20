# Cognify AI — Project Specification

## 1. Overview

Cognify AI is an Agentic AI + NLP-based reading and recall assessment application.

The user selects:

- Topic
- Word limit
- Difficulty
- Reading time
- Writing time

The AI generates a passage. The user reads it within the given time and then writes a summary from memory. The system evaluates the response using NLP techniques and AI agents.

---

## 2. Core Workflow

User Settings
     ↓
Content Generation Agent
     ↓
Content Validation
     ↓
Reading Phase + Timer
     ↓
Passage Disappears
     ↓
Recall Phase + Timer
     ↓
User Summary
     ↓
Evaluation Agent
     ↓
NLP Analysis
     ↓
Scoring
     ↓
AI Feedback

---

## 3. Evaluation

The response will be evaluated on:

- **Semantic Similarity** — Does the summary capture the original meaning?
- **Information Coverage** — How many important concepts were recalled?
- **Factual Accuracy** — Does the response contradict the original?
- **Language Quality** — Grammar, readability and writing quality.
- **Coherence** — How logically is the summary presented?

Initial scoring:

| Metric | Weight |
|---|---:|
| Semantic Understanding | 30% |
| Information Coverage | 30% |
| Factual Accuracy | 20% |
| Language Quality | 10% |
| Coherence | 10% |

The final score should be calculated through a scoring engine rather than allowing an LLM to arbitrarily assign marks.

---

## 4. Agentic AI

### Content Generation Agent

Generates the passage based on:

Topic + Word Limit + Difficulty

It should also provide important concepts that can later be used for evaluation.

### Evaluation Agent

Coordinates the different NLP evaluation components and produces the evaluation result.

### AI Feedback

An LLM generates human-readable feedback based on the calculated evaluation scores.

---

## 5. NLP Components

The project should demonstrate practical NLP concepts:

- Text Embeddings
- Semantic Similarity
- Information/Concept Coverage
- Natural Language Inference
- Text/Language Analysis

LLMs should not be used for every task.

---

## 6. Project Structure

mindmark/
│
├── PROJECT_SPEC.md
├── app.py
├── config.py
├── requirements.txt
├── .env
│
├── agents/
│   ├── content_agent.py
│   └── evaluation_agent.py
│
├── nlp/
│   ├── embeddings.py
│   ├── similarity.py
│   ├── coverage.py
│   └── nli.py
│
├── evaluation/
│   └── scoring.py
│
├── models/
│   ├── llm.py
│   ├── embedding_model.py
│   └── nli_model.py
│
└── utils/
    └── timer.py

The structure should remain small initially. New folders/files should only be introduced when a future feature actually requires them.

---

## 7. MVP Goal

The first working version must support:

**Generate → Read → Recall → NLP Evaluation → Score → Feedback**

Future features such as:

- User history
- Adaptive difficulty
- Leaderboards
- Authentication
- Multiple challenge modes
- Database

will be considered after the MVP.