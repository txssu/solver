@echo off
set VENV=venv
if not exist %VENV%\Scripts\python.exe (
    python -m venv %VENV%
)
%VENV%\Scripts\pip install -r requirements.txt
%VENV%\Scripts\python -m streamlit run dashboard.py
