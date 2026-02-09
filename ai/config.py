# config.py - AI Service Configuration
#
# Settings for AI services and API keys.

"""
Configuration

Settings:
- OPENAI_API_KEY
- ANTHROPIC_API_KEY
- GOOGLE_VISION_API_KEY
- TESSERACT_PATH
- MODEL_CACHE_DIR
"""

import os
from pathlib import Path

# LLM API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Google Cloud
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# OCR
TESSERACT_PATH = os.getenv("TESSERACT_PATH", "/usr/bin/tesseract")

# Model Cache
MODEL_CACHE_DIR = os.getenv("MODEL_CACHE_DIR", "./models/cache")
Path(MODEL_CACHE_DIR).mkdir(parents=True, exist_ok=True)

# Service Config
AI_SERVICE_PORT = int(os.getenv("AI_SERVICE_PORT", "8001"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
