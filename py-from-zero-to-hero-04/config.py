import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base config"""
    APP_BACKEND_URL = os.environ.get("APP_BACKEND_URL", "")
    PORT = os.environ.get("APP_PORT", 5000)

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

## Current config
config_class = DevelopmentConfig if os.environ.get("APP_ENV") == "development" else ProductionConfig