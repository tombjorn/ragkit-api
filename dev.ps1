# dev.ps1 - Restart RAGKit API (Windows / PowerShell)

Write-Host "Restarting RAGKit API..." -ForegroundColor Cyan

# Activate venv
& .\venv\Scripts\Activate.ps1

# Start API with reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000
