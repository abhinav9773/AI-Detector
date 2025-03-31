import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Print API Keys to check if they are loaded correctly
print("Google API Key:", os.getenv("GOOGLE_FACTCHECK_API_KEY"))
print("OpenAI API Key:", os.getenv("OPENAI_API_KEY"))
