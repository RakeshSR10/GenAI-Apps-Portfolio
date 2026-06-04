from dotenv import load_dotenv, find_dotenv
import os

# 🔥 FORCE FIND .env FILE
dotenv_path = find_dotenv()

print("FOUND .env AT:", dotenv_path)

load_dotenv(dotenv_path, override=True)

print("KEY =", repr(os.getenv("GOOGLE_API_KEY")))