# Cognify AI — Implementation & Scalability Notes

> Internal technical notes for revising the project architecture.
> This is not the public README.

---

# 1. Current Implementation

Cognify AI is a Streamlit-based cognitive recall application.

The complete flow is:

    Setup
      ↓
    Content Generation
      ↓
    Content Validation
      ↓
    Reading
      ↓
    Recall
      ↓
    Evaluation Graph
      ↓
    Final Evaluation
      ↓
    Result


## 2. Content Generation

Content generation is implemented as a separate LangGraph:

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

The generator creates:

- Reading passage
- Key concepts
- Topic
- Difficulty

The validator checks:

- Word count
- Topic relevance
- Coherence
- Difficulty
- Sufficient information

Word count is calculated deterministically using Python, while qualitative
validation is performed by the LLM.


# 3. Reading & Recall

Streamlit manages the user-facing phases using:

    st.session_state.stage

Stages:

    setup
    reading
    recall
    evaluation
    result

The reading and recall timers use:

    st.fragment(run_every=1)

instead of `st_autorefresh()`.

This prevents the entire Streamlit application from rerunning every second.

The recall textarea is synchronized with Streamlit session state so that
typed content is not lost when the timer expires.

Recall can finish through:

- Timer expiry
- Submit Recall button

The finalized response is stored as:

    st.session_state.user_recall


# 4. Evaluation Graph

The Evaluation Graph is a separate LangGraph.

The four evaluation agents run independently and in parallel:

                    START
                      │
        ┌─────────────┼─────────────┐
        ↓             ↓             ↓
     Semantic      Coverage     Faithfulness
        │             │             │
        └─────────────┼─────────────┘
                      ↓
               Language Coherence
                      │
                      ↓
               Final Evaluator
                      │
                      ↓
                     END

The graph receives:

    original_text
    key_concepts
    recall_text


# 5. Evaluation Agents

## Semantic Similarity

Uses sentence embeddings to compare the overall meaning of the original
passage and recall.

Model:

    all-MiniLM-L6-v2


## Concept Coverage

Compares each generated key concept against the user's recall.

It identifies:

    covered_concepts
    missed_concepts
    coverage_score


## Faithfulness

Faithfulness uses a two-step approach:

    Recall sentence
          ↓
    Find best matching source sentence
          ↓
    NLI classification
          ↓
    entailment / neutral / contradiction

NLI model:

    cross-encoder/nli-MiniLM2-L6-H768

This prevents the NLI model from comparing every recall sentence against the
entire passage.


## Language Coherence

Evaluates:

- Grammar
- Clarity
- Coherence
- Organization

This is intentionally separate from memory accuracy.


## Final Evaluator

The Final Evaluator receives:

    semantic_result
    concept_coverage_result
    faithfulness_result
    language_coherence_result

and produces:

    final_score
    performance_level
    strengths
    missed_areas
    feedback


# 6. Technology Stack

    Python
    Streamlit
    LangGraph
    Pydantic
    OpenAI API
    Sentence Transformers
    PyTorch
    Hugging Face


# 7. Why the Architecture Is Split

Content generation and evaluation are maintained as two separate graphs.

Content Graph:

    Generate → Validate → Regenerate if necessary

Evaluation Graph:

    Parallel Evaluation → Final Evaluator

This keeps the system modular and makes individual components easier to test,
replace, and scale.


# 8. Future Scalability Plan

The current application is primarily a Streamlit prototype.

The planned production architecture is:

                  Frontend
                     │
                     ▼
                  Backend API
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
    Content Graph        Evaluation Graph
          │                     │
          └──────────┬──────────┘
                     ▼
                  Database


## Phase 1 — Backend Separation

Move the application logic out of Streamlit into an API layer.

Possible architecture:

    Streamlit / Web UI
           ↓
        FastAPI
           ↓
    LangGraph workflows


## Phase 2 — Persistence

Add a database to store:

- Users
- Generated challenges
- Recall responses
- Evaluation results
- Historical scores

This will allow users to track improvement over time.


## Phase 3 — Scalable Model Execution

Separate model inference from the web application.

Potentially use:

    API service
        ↓
    Worker / inference service
        ↓
    ML models

This prevents heavy model execution from blocking the main application.


## Phase 4 — Async / Distributed Evaluation

The four evaluation agents are already architecturally independent.

They can eventually be executed using distributed workers or asynchronous
jobs when user traffic increases.


## Phase 5 — Adaptive Challenges

Use historical evaluation results to dynamically adjust:

- Difficulty
- Word limit
- Reading time
- Topic complexity

This can turn Cognify into a personalized cognitive training system.


## Phase 6 — Production Infrastructure

Future production deployment can include:

- Docker
- AWS
- CI/CD
- Model/version management
- Logging
- Monitoring
- Error tracking
- Database backups
- Authentication

The final target architecture is therefore:

    User
      ↓
    Frontend
      ↓
    API
      ↓
    LangGraph Orchestration
      ↓
    ┌───────────────┬────────────────┐
    │               │                │
 Content Graph  Evaluation Graph  Other Services
    │               │
    └───────┬───────┘
            ↓
       ML / LLM Services
            ↓
         Database