"""Application configuration (scaffold)."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class Config:
    """Base configuration."""

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"
