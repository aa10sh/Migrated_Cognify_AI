from pathlib import Path

files = [
    "app.py",
    "config.py",
    "requirements.txt",
    ".env",
    "PROJECT_SPEC.md",

    "agents/__init__.py",
    "agents/content_agent.py",
    "agents/evaluation_agent.py",

    "nlp/__init__.py",
    "nlp/embeddings.py",
    "nlp/similarity.py",
    "nlp/coverage.py",
    "nlp/nli.py",

    "evaluation/__init__.py",
    "evaluation/scoring.py",

    "models/__init__.py",
    "models/llm.py",
    "models/embedding_model.py",
    "models/nli_model.py",

    "utils/__init__.py",
    "utils/timer.py",
]

for file in files:
    path = Path(file)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)

print("Cognify AI project structure created successfully!")