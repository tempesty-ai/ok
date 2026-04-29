@echo off
setlocal
cd /d "%~dp0playwright"

call :find_python
if errorlevel 1 exit /b 1

echo [INFO] Installing Playwright dependencies...
"%PYTHON_CMD%" -m pip install -r requirements.txt
if errorlevel 1 (
  echo [ERROR] Dependency install failed.
  exit /b 1
)

echo [INFO] Installing Playwright browsers...
"%PYTHON_CMD%" -m playwright install
if errorlevel 1 (
  echo [ERROR] Browser install failed.
  exit /b 1
)

echo [INFO] Running Playwright tests...
"%PYTHON_CMD%" -m pytest
exit /b %errorlevel%

:find_python
set "PYTHON_CMD="
python --version >nul 2>&1
if not errorlevel 1 set "PYTHON_CMD=python"

if not defined PYTHON_CMD (
  py --version >nul 2>&1
  if not errorlevel 1 set "PYTHON_CMD=py"
)

if not defined PYTHON_CMD (
  echo [ERROR] Python was not found.
  echo Install Python 3.10+ from https://www.python.org/downloads/
  echo During install, check "Add python.exe to PATH".
  exit /b 1
)
exit /b 0
