@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Run: py -3 -m venv .venv
  pause
  exit /b 1
)
".venv\Scripts\python.exe" -m mkdocs build --strict
if errorlevel 1 exit /b 1
echo Build complete: site\index.html
pause
