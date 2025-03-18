# config.py
import os
from dotenv import load_dotenv

# Load variables from .env if present
load_dotenv()

ENV = os.getenv("ENV", "development")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not JWT_SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY environment variable not set")
