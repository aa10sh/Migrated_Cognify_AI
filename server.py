import os
from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import set_key

from config import (
    APP_NAME,
    WORD_LIMITS,
    DIFFICULTIES,
    READING_TIMES,
    WRITING_TIMES,
)
from agents.content_agent import generate_challenge
from graph.evaluation_graph import evaluation_graph
from models.llm import is_api_key_configured, get_model_name, get_api_key

app = FastAPI(title=APP_NAME, description="CognifyAI LangGraph Evaluation and Memory Challenge API")

# Enable CORS for local React development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------------------------------------------
# Request & Response Schemas
# -----------------------------------------------------------------------------

class GenerateChallengeRequest(BaseModel):
    topic: str
    word_limit: int = 150
    difficulty: str = "Medium"


class ChallengeResponse(BaseModel):
    topic: str
    content: str
    word_count: int
    difficulty: str
    key_concepts: List[str]


class EvaluateChallengeRequest(BaseModel):
    original_text: str
    key_concepts: List[str]
    recall_text: str


class SettingsUpdateRequest(BaseModel):
    openai_api_key: Optional[str] = None
    openai_model: Optional[str] = None


# -----------------------------------------------------------------------------
# API Endpoints
# -----------------------------------------------------------------------------

@app.get("/api/health")
def health():
    return {"status": "ok", "app": APP_NAME}


@app.get("/api/config")
def get_config():
    return {
        "app_name": APP_NAME,
        "word_limits": WORD_LIMITS,
        "difficulties": DIFFICULTIES,
        "reading_times": READING_TIMES,
        "writing_times": WRITING_TIMES,
        "has_api_key": is_api_key_configured(),
        "model_name": get_model_name(),
    }


@app.post("/api/settings")
def update_settings(payload: SettingsUpdateRequest):
    env_path = Path(".env")
    if not env_path.exists():
        env_path.touch()

    if payload.openai_api_key is not None:
        key = payload.openai_api_key.strip()
        os.environ["OPENAI_API_KEY"] = key
        set_key(str(env_path), "OPENAI_API_KEY", key)

    if payload.openai_model is not None:
        model = payload.openai_model.strip()
        if model:
            os.environ["OPENAI_MODEL"] = model
            set_key(str(env_path), "OPENAI_MODEL", model)

    return {
        "success": True,
        "has_api_key": is_api_key_configured(),
        "model_name": get_model_name(),
    }


@app.post("/api/challenge/generate", response_model=ChallengeResponse)
def api_generate_challenge(req: GenerateChallengeRequest):
    if not req.topic.strip():
        raise HTTPException(status_code=400, detail="Topic cannot be empty")

    try:
        challenge = generate_challenge(
            topic=req.topic.strip(),
            word_limit=req.word_limit,
            difficulty=req.difficulty,
        )
        return ChallengeResponse(
            topic=challenge.topic,
            content=challenge.content,
            word_count=challenge.word_count,
            difficulty=challenge.difficulty,
            key_concepts=challenge.key_concepts,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Challenge generation error: {str(e)}")


@app.post("/api/challenge/evaluate")
def api_evaluate_challenge(req: EvaluateChallengeRequest):
    try:
        clean_recall = req.recall_text.strip() if req.recall_text else ""
        # LangGraph parallel multi-agent evaluation execution
        result = evaluation_graph.invoke(
            {
                "original_text": req.original_text,
                "key_concepts": req.key_concepts,
                "recall_text": clean_recall,
            }
        )
        return {
            "semantic_result": result.get("semantic_result", {}),
            "concept_coverage_result": result.get("concept_coverage_result", {}),
            "faithfulness_result": result.get("faithfulness_result", {}),
            "language_coherence_result": result.get("language_coherence_result", {}),
            "final_result": result.get("final_result", {}),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LangGraph evaluation error: {str(e)}")


# -----------------------------------------------------------------------------
# Static files / Production build serving
# -----------------------------------------------------------------------------
dist_path = Path("frontend/dist")
if dist_path.exists():
    app.mount("/assets", StaticFiles(directory=str(dist_path / "assets")), name="assets")

    @app.get("/{full_path:path}")
    def serve_frontend(full_path: str):
        file_candidate = dist_path / full_path
        if file_candidate.is_file():
            return FileResponse(file_candidate)
        return FileResponse(dist_path / "index.html")


if __name__ == "__main__":
    import uvicorn
    print(f"Starting {APP_NAME} server on http://localhost:8000...")
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
