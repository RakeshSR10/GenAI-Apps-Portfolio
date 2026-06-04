import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.tools import DuckDuckGoSearchRun

# 1. Dynamically locate the global .env file at the workspace root level (4 levels up)
root_dir = Path(__file__).resolve().parents[3] 
env_path = root_dir / '.env'

# 2. Load the global .env file with override enabled
load_dotenv(dotenv_path=env_path, override=True)

def search_internet(query: str) -> str:
    """
    Searches the live web using DuckDuckGo and returns text summaries.
    No external search API keys are required for this tool.
    """
    try:
        search = DuckDuckGoSearchRun()
        results = search.run(query)
        return results
    except Exception as e:
        return f"Web search tool failed to fetch data: {str(e)}"
