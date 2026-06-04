import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Dynamically locate the global .env file at the workspace root level
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

# Prompt template for Translation
prompt = PromptTemplate(
    template='''
        Translate the following text into {language}.
        Only give translated output.
        No explanation.
        No numbering.
        No transliteration.

        Text: {text} ''',
    input_variables=['language', 'text']
)

# Parser
parser = StrOutputParser()

# Chain
chain = prompt | llm | parser

# User Input
text = input("Enter Your text:- ")
language = input("Enter Your language:- ")

# Invoke Chain
result = chain.invoke({
    'language': language,
    'text': text
})

# Output
print("\n===== TRANSLATED TEXT =====\n")
print(result)
