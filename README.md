# 🚀 AI Text Summarizer App

A beginner Generative AI project built using:

- LangChain
- Google Gemini API
- Python

This application summarizes large text into short concise summaries using Google's Gemini LLM.

---

# 📌 Project Goal

The goal of this project is to learn:

- Generative AI basics
- LangChain fundamentals
- Prompt Engineering
- LCEL chaining
- Gemini API integration
- Environment variable handling
- Virtual Environment setup

---

# 🧠 Technologies Used

| Technology    | Purpose                    |
| ------------- | -------------------------- |
| Python        | Programming Language       |
| LangChain     | LLM Framework              |
| Gemini API    | Large Language Model       |
| python-dotenv | Load environment variables |

---

# 📂 Project Structure

```bash
01_TextSummerizerApp/
│
├── venv/
├── app.py
├── .env
├── requirements.txt
├── README.md
```

---

# ⚙️ Complete Setup From Scratch

---

# ✅ Step 1 — Create Project Folder

Open VS Code terminal or CMD and run:

```bash
mkdir 01_TextSummerizerApp
cd 01_TextSummerizerApp
```

---

# ✅ Step 2 — Open VS Code

```bash
code .
```

---

# ✅ Step 3 — Create Virtual Environment

Run:

```bash
python -m venv venv
```

This creates a virtual environment folder named `venv`.

---

# ✅ Step 4 — Activate Virtual Environment

## ▶️ Windows PowerShell

```powershell
venv\Scripts\activate
```

---

## ▶️ Windows CMD

```cmd
venv\Scripts\activate.bat
```

---

## ▶️ Git Bash

```bash
source venv/Scripts/activate
```

---

# ✅ After Activation

Terminal becomes:

```bash
(venv) PS C:\PythonPracs\Apps\01_BeginnerApps\01_TextSummerizerApp>
```

⚠️ `(venv)` must appear before proceeding.

---

# ✅ Step 5 — Create `requirements.txt`

Create file:

```bash
requirements.txt
```

Add:

```txt
langchain
langchain-google-genai
python-dotenv
```

---

# ✅ Step 6 — Install Required Packages

Run:

```bash
pip install -r requirements.txt
```

This installs:

- LangChain
- Gemini integration
- dotenv package

---

# 🔑 Gemini API Setup

---

# ✅ Step 7 — Generate Gemini API Key

Go to:

https://aistudio.google.com/app/apikey

Steps:

1. Login with Google account
2. Click `Create API Key`
3. Copy API key

Example:

```txt
AIzaSyXXXXXXXXXXXX
```

---

# ✅ Step 8 — Create `.env` File

Create file:

```bash
.env
```

Add:

```env
GOOGLE_API_KEY=your_gemini_api_key
```

⚠️ Important:

- No quotes
- No spaces
- Keep `.env` secret

❌ Wrong:

```env
GOOGLE_API_KEY="AIza..."
```

✅ Correct:

```env
GOOGLE_API_KEY=AIza...
```

---

# ✅ Step 9 — Create `app.py`

Create file:

```bash
app.py
```

Add the following code:

```python
from dotenv import load_dotenv
import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load .env
load_dotenv(override=True)

# Read API key
api_key = os.getenv("GOOGLE_API_KEY")

# Debug
print("Loaded Key:", api_key[:10])

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
```

---

# ▶️ Step 10 — Run Application

Run:

```bash
python app.py
```

---

# ✅ Expected Output

```bash
===== RESULT =====

Artificial Intelligence is transforming the world through automation and smart systems.
A key development, Generative AI, can create text, images, code, and videos.
```

---

# 🧠 Concepts Learned

---

# ✅ Virtual Environment (`venv`)

Used to isolate project dependencies.

Benefits:

- No package conflicts
- Clean project setup
- Professional workflow

---

# ✅ `.env` File

Used to securely store:

- API keys
- Secret credentials

Loaded using:

```python
load_dotenv()
```

---

# ✅ PromptTemplate

Used to create dynamic prompts for LLMs.

Example:

```python
prompt = PromptTemplate(
    template="Summarize:\n{text}",
    input_variables=["text"]
)
```

---

# ✅ ChatGoogleGenerativeAI

Connects LangChain with Gemini API.

---

# ✅ StrOutputParser

Converts model output into plain text.

---

# ✅ LCEL Chain

```python
chain = prompt | llm | parser
```

Pipeline flow:

```text
Input → Prompt → Gemini Model → Parser → Output
```

---

# ✅ Deactivate Virtual Environment

When finished:

```bash
deactivate
```

---

# 🚀 Future Improvements

Possible upgrades:

- Streamlit UI
- User input from terminal
- PDF summarizer
- Website summarizer
- YouTube summarizer

---

# 📚 Learning Outcome

After completing this project learned:

- How to use Gemini API
- How LangChain works
- How to create LCEL chains
- How to manage API keys securely
- How to use PromptTemplate
- How to build a GenAI application from scratch

---

# 👨‍💻 Author

Rakesh S R

Generative AI Learning Journey 🚀
