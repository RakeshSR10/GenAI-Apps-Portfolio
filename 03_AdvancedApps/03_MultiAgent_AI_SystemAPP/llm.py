import os
import warnings
from pathlib import Path
from dotenv import load_dotenv

# Suppress developer deprecation warnings completely right at the start
warnings.filterwarnings("ignore", category=DeprecationWarning)

from langchain_google_genai import ChatGoogleGenerativeAI

# 1. Dynamically locate the global .env file at the workspace root level (4 levels up)
# Path jumps up: 03_MultiAgent_AI_SystemAPP -> 03_AdvancedApps -> Apps -> PythonPracs
root_dir = Path(__file__).resolve().parents
env_path = root_dir / '.env'

# 2. Load the global .env file with override enabled
load_dotenv(dotenv_path=env_path, override=True)

# Read API key securely
api_key = os.getenv("GOOGLE_API_KEY")

# Low temperature ensures strict compliance with our agent role instructions
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=api_key,
    temperature=0.2 
)
