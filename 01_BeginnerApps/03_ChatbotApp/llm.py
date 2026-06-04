import os
from pathlib import Path
from dotenv import load_dotenv

# 1. Dynamically locate the global .env file at the workspace root level
# Adjust parents[2] if your folder nesting depth changes
root_dir = Path(__file__).resolve().parents[2] 
env_path = root_dir / '.env'

# 2. Load the global .env file with override enabled
load_dotenv(dotenv_path=env_path, override=True)

api_key = os.getenv("GOOGLE_API_KEY")

from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=api_key
)
