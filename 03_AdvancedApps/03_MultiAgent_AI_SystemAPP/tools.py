import os
import warnings
from pathlib import Path
from dotenv import load_dotenv

# Suppress all deprecation warning messages immediately at compilation time
warnings.filterwarnings("ignore", category=DeprecationWarning)

from langchain_community.tools import DuckDuckGoSearchRun

# 1. Dynamically locate the global .env file at the workspace root level
root_dir = Path(__file__).resolve().parents
env_path = root_dir / '.env'

# 2. Load the global .env file with override enabled
load_dotenv(dotenv_path=env_path, override=True)

# Initialize the free DuckDuckGo search tool wrapper
web_search_tool = DuckDuckGoSearchRun()

def search_internet(query: str) -> str:
    """
    Searches the live internet for a given topic and returns summary text snippets.
    """
    try:
        # Executes the web search and returns raw text data results
        results = web_search_tool.run(query)
        return results
    except Exception as e:
        return f"--Search engine error occurred: {str(e)}"

if __name__ == "__main__":
    print("Testing Web Search Engine...")
    test_results = search_internet("Latest global tech breakthroughs 2026")
    print(test_results)
