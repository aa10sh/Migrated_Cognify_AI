@echo off
title CognifyAI (React + LangGraph)
echo ===================================================
echo 🧠 Starting Cognify AI (React + LangGraph)
echo ===================================================

if not exist "venv\Scripts\python.exe" (
    echo Python virtual environment not found. Please run: py -3.11 -m venv venv
    pause
    exit /b 1
)

.\venv\Scripts\python.exe run.py
pause
