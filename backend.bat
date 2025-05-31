@echo off


start "RAG" cmd /k  ".\.venv\Scripts\python.exe chromadb_helper.py"
start "LLM" cmd /k  ".\.venv\Scripts\python.exe manage.py"


exit