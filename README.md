# Cognify AI

Cognify AI is an AI-powered cognitive recall application that evaluates how well a user can remember and reproduce information after reading a passage for a limited amount of time.

Instead of relying on a single similarity score, Cognify evaluates recall across multiple dimensions:

- Semantic Similarity
- Concept Coverage
- Faithfulness
- Language Coherence

The results are combined to generate a final score, performance level, and personalized feedback.

## How It Works

```text
Setup
  ↓
Content Generation
  ↓
Content Validation
  ↓
Reading Phase
  ↓
Recall Phase
  ↓
Evaluation Graph
  ├── Semantic Similarity
  ├── Concept Coverage
  ├── Faithfulness
  └── Language Coherence
          ↓
    Final Evaluator
          ↓
    Result & Feedback
```

### Content Generation

The user selects a topic, word limit, difficulty, reading time, and recall time.

The Content Generation Graph then:

1. Generates a reading passage.
2. Extracts important key concepts.
3. Validates the generated content.
4. Regenerates the content if validation fails.

### Reading and Recall

The user reads the generated passage within the configured time limit.

After the reading phase, the passage disappears and the user writes everything they remember during the recall phase.

The recall can be submitted manually or automatically when the timer expires.

## Evaluation System

Cognify uses four independent evaluation agents.

| Evaluation | Purpose |
|---|---|
| Semantic Similarity | Measures similarity in overall meaning |
| Concept Coverage | Measures how many important concepts were remembered |
| Faithfulness | Checks whether recalled claims are supported by the original passage |
| Language Coherence | Evaluates grammar, clarity, coherence, and organization |

The four agents are designed to run in parallel using LangGraph. Their results are then passed to a Final Evaluator that generates the overall result.

### Semantic Similarity

Uses sentence embeddings to compare the meaning of the original passage and the user's recall.

Model:

```text
sentence-transformers/all-MiniLM-L6-v2
```

### Concept Coverage

Compares the important concepts extracted from the original passage with the user's recall and identifies covered and missed concepts.

### Faithfulness

Checks whether recalled statements are supported by the original passage.

The system finds the most relevant source sentence and uses an NLI model to classify the relationship as:

- Entailment
- Neutral
- Contradiction

Model:

```text
cross-encoder/nli-MiniLM2-L6-H768
```

### Language Coherence

Evaluates the quality of the written recall based on:

- Grammar
- Clarity
- Coherence
- Organization

## Architecture

Cognify uses two separate LangGraph workflows.

### Content Generation Graph

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

### Evaluation Graph

```text
                 START
                   │
        ┌──────────┼──────────┐
        ↓          ↓          ↓
    Semantic    Coverage   Faithfulness
        │          │          │
        └──────────┼──────────┘
                   ↓
           Language Coherence
                   ↓
            Final Evaluator
                   ↓
                  END
```

## Technology Stack

- Python
- Streamlit
- LangGraph
- Pydantic
- OpenAI API
- Sentence Transformers
- PyTorch
- Hugging Face

## Project Structure

```text
CognifyAI/
│
├── agents/
│   ├── content_agent.py
│   ├── content_validator_agent.py
│   ├── semantic_agent.py
│   ├── coverage_agent.py
│   ├── faithfulness_agent.py
│   ├── language_coherence_agent.py
│   └── final_evaluator_agent.py
│
├── graph/
│   ├── content_graph.py
│   └── evaluation_graph.py
│
├── nlp/
│   ├── embeddings.py
│   ├── coverage.py
│   ├── nli.py
│   └── faithfulness.py
│
├── models/
│   ├── challenge.py
│   └── llm.py
│
├── app.py
├── config.py
└── requirements.txt
```

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd CognifyAI
```

Create a virtual environment:

```bash
python -m venv cognify
```

Activate it on Windows:

```powershell
.\cognify\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```text
OPENAI_API_KEY=your_api_key
```

Run the application:

```bash
streamlit run app.py
```

## Future Plans

- Backend API using FastAPI
- Database integration
- User accounts and progress tracking
- Adaptive difficulty based on previous performance
- Asynchronous and distributed evaluation
- Dedicated ML inference services
- Docker and AWS deployment
- CI/CD pipeline
- Logging and monitoring

The long-term goal is to evolve Cognify into a personalized cognitive training platform that adapts challenges based on the user's previous performance.

## Author

**Adarsh Singh**
