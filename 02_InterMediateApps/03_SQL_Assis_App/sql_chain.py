import re
from llm import llm
from database import run_sql_query

def get_db_schema():
    """Returns the strict database column structural layout for the LLM prompt."""

    schema = """
    Table: EMPLOYEES
    Columns:
    - ID: INTEGER (Primary Key)
    - NAME: TEXT (Employee's full name)
    - DEPARTMENT: TEXT ('Engineering', 'Sales', 'HR', 'Marketing')
    - ROLE: TEXT (Job title description e.g., 'Senior Developer')
    - SALARY: INTEGER (Annual compensation metric value)
    - JOIN_DATE: TEXT (Format: 'YYYY-MM-DD')
    """
    return schema

def generate_clean_sql(user_question):
    """Translates the text question into an isolated executable SQLite statement."""
    schema = get_db_schema()

    prompt = f"""
        You are an expert SQL generation assistant.
        Given a user question and a database schema, write a clean, 
        valid SQLite query to answer the question.
        
        Database Schema Layout: {schema}
        
        Rules:
        1. Output ONLY the raw SQL query string. 
        2. Do NOT wrap the query in markdown code blocks like ```sql or ```.
        3. Do NOT include any explanations, introduction words, or trailing text.
        4. Only query the columns defined in the schema layout above.
        
        Question: {user_question}
        """
        # Generate syntax via gemini-2.5-flash
    raw_response = llm.invoke(prompt).content.strip()
    
    # Safe regex fallback filter to strip out markdown blocks if the LLM adds them
    clean_query = re.sub(r"```[a-zA-Z]*\n|```", "", raw_response).strip()
    return clean_query

def generate_final_explanation(user_question, sql_query, sql_results):
    """Feeds raw database tuple structures back to Gemini to draft an English answer."""
    prompt = f"""
    You are an intelligent corporate data analyst assistant. 
    Analyze the raw database results provided below and translate them into a clear, helpful, natural English answer matching the user's question.
    
    User Original Question: {user_question}
    Executed SQL Query Syntax: {sql_query}
    Raw SQL Execution Tuple Results: {sql_results}
    
    Guidelines:
    - Present numbers, salaries, or names cleanly.
    - If the results are empty, say "No matching employee records found."
    - Keep your explanation direct and easy to read.
    """
    
    explanation = llm.invoke(prompt).content.strip()
    return explanation