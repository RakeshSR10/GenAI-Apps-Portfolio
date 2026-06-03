import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Dynamically locate the global .env file at the root level
# Adjust parents[2] if your directory nesting depth changes
root_dir = Path(__file__).resolve().parents[2] 
env_path = root_dir / '.env'

# 2. Load the global .env file with override enabled
load_dotenv(dotenv_path=env_path, override=True)

# Read API key
api_key = os.getenv("GOOGLE_API_KEY")

# Gemini Model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=api_key
)

# Prompt
prompt = PromptTemplate(
    template="Summarize the following text in 2 lines:\n{text}",
    input_variables=["text"]
)

# Parser
parser = StrOutputParser()

# Chain
chain = prompt | llm | parser

# Input text
text_data = """
Artificial Intelligence is changing the world through automation and smart systems.
Generative AI can create text, images, code, and videos.
"""

# Invoke
result = chain.invoke({"text": text_data})

# Output
print("\n===== RESULT =====\n")
print(result)
