@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Run: py -3 -m venv .venv
  pause
  exit /b 1
)
".venv\Scripts\python.exe" -m mkdocs serve --dev-addr 127.0.0.1:8008
pause
