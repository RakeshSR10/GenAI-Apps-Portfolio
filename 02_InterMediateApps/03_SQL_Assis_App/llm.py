import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# 1. Dynamically locate the global .env file at the workspace root level (4 levels up)
# Path jumps up: 03_SQL_Assis_App -> 02_IntermediateApps -> Apps -> PythonPracs
root_dir = Path(__file__).resolve().parents 
env_path = root_dir / '.env'

# 2. Load the global .env file with override enabled
load_dotenv(dotenv_path=env_path, override=True)

# Read API key securely
api_key = os.getenv("GOOGLE_API_KEY")

# Gemini Model setup configured with 0.1 temperature for strict deterministic SQL outputs
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=api_key,
    temperature=0.1
)
