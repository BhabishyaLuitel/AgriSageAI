import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Gemini AI Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_MODEL = 'gemini-1.5-flash'  # Valid models: gemini-1.5-flash, gemini-1.5-pro

# Flask Configuration
FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-here')
FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'

# Model Configuration
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload size
