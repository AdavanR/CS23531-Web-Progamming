"""
Global configuration for PromptGuard.
"""

import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

# Default Model Provider Settings
DEFAULT_PROVIDER = "simulator"  # "simulator", "ollama", "openai"
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "mistral:7b")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Server Config
API_HOST = os.getenv("PROMPTGUARD_API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("PROMPTGUARD_API_PORT", 8000))
UI_PORT = int(os.getenv("PROMPTGUARD_UI_PORT", 8501))
