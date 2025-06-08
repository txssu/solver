@echo off
set VENV=venv
if not exist %VENV%\Scripts\python.exe (
    python -m venv %VENV%
)
%VENV%\Scripts\pip install -r requirements.txt
%VENV%\Scripts\python run_planning.py
