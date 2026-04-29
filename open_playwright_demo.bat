@echo off
setlocal
cd /d "%~dp0playwright"
start "" "%CD%\demo_page.html"

