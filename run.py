"""
CognifyAI Launch Script
Runs the FastAPI LangGraph backend server and opens the React application.
"""
import os
import sys
import subprocess
import time
import webbrowser

VENV_PYTHON = os.path.join(os.path.dirname(__file__), "venv", "Scripts", "python.exe")
if not os.path.exists(VENV_PYTHON):
    VENV_PYTHON = sys.executable

def main():
    print("=" * 60)
    print("🧠 CognifyAI — React Frontend + LangGraph Backend")
    print("=" * 60)
    
    # Check if frontend/dist exists, if not build it
    dist_index = os.path.join("frontend", "dist", "index.html")
    if not os.path.exists(dist_index):
        print("Building React frontend distribution...")
        subprocess.run(["npm.cmd", "run", "build"], cwd="frontend", check=True)
    
    print("\nStarting Unified Server on http://localhost:8000...")
    print("Backend: FastAPI + LangGraph + SentenceTransformers")
    print("Frontend: React + Tailwind CSS (served directly)")
    print("\nOpening web browser...")
    webbrowser.open("http://localhost:8000")
    
    # Run uvicorn server
    subprocess.run([VENV_PYTHON, "-m", "uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])

if __name__ == "__main__":
    main()
