import os
from dotenv import load_dotenv

load_dotenv()

# Load API keys from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Default LLM Settings
DEFAULT_MODEL = "llama3-8b-8192"
DEFAULT_EMBEDDING_MODEL = "models/embedding-001"
DEFAULT_TEMPERATURE = 0.0
