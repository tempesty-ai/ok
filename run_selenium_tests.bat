@echo off
setlocal
cd /d "%~dp0selenium"

call :find_python
if errorlevel 1 exit /b 1

echo [INFO] Installing Selenium dependencies...
"%PYTHON_CMD%" -m pip install -r requirements.txt
if errorlevel 1 (
  echo [ERROR] Dependency install failed.
  exit /b 1
)

echo [INFO] Running Selenium demo test...
"%PYTHON_CMD%" test_demo.py
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

