@echo off
title PromptGuard - REST API Server
echo =======================================================
echo   PromptGuard - REST API Server
echo =======================================================
echo.
echo Starting FastAPI REST Server at http://127.0.0.1:8000 ...
echo Swagger UI docs available at: http://127.0.0.1:8000/docs
echo.

set PYTHONPATH=%~dp0
python run.py --api

pause
