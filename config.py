"""Application configuration loaded from environment variables."""
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

# Load .env file if it exists
load_dotenv(BASE_DIR / ".env")


class Config:
    """Base configuration."""

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

    # Database
    DB_DRIVER = os.getenv("DB_DRIVER", "mysql").lower()
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "pemetaan_digital_jabar")

    # SQLite fallback path
    SQLITE_PATH = str(BASE_DIR / "pemetaan_digital_jabar.sqlite3")

    # Uploads
    UPLOAD_FOLDER = str(BASE_DIR / os.getenv("UPLOAD_FOLDER", "uploads"))
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", str(16 * 1024 * 1024)))
    ALLOWED_EXTENSIONS = {"xlsx", "xls", "csv"}

    # Flask
    DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"

    # Indikator (variabel) yang digunakan untuk clustering
    INDIKATOR = ["internet", "laptop", "smartphone", "literasi_digital"]

    # Tahun data (PRD 2.2 — data 2023)
    DEFAULT_TAHUN = 2023
