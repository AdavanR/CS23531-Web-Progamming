@echo off
title PromptGuard - Prompt Injection Testing Sandbox
echo =======================================================
echo   PromptGuard - Prompt Injection Testing Sandbox
echo =======================================================
echo.
echo Starting PromptGuard Web Dashboard...
echo.

set PYTHONPATH=%~dp0
python run.py

pause
