import streamlit as st
from database import init_database, run_sql_query
from sql_chain import generate_clean_sql, generate_final_explanation

# Page setup
st.set_page_config(page_title="SQL AI Assistant", page_icon="🗄️")
st.title("🗄️ SQL Database AI Assistant (Text-to-SQL)")
st.subheader("Chat directly with your Corporate Employee Database using Gemini 2.5")

# Initialize database file and dummy records upon first startup rerun
if "db_initialized" not in st.session_state:
    init_database()
    st.session_state.db_initialized = True

# Display Schema Information in Sidebar for User Reference
with st.sidebar:
    st.markdown("### 📊 Database Schema Details")
    st.markdown("""
    **Table:** `EMPLOYEES`
    - `ID`: Unique Identifier
    - `NAME`: Full Name
    - `DEPARTMENT`: Dept Group
    - `ROLE`: Job Title Description
    - `SALARY`: Annual Compensation
    - `JOIN_DATE`: 'YYYY-MM-DD'
    """)
    st.write("---")
    st.info("Sample Departments:\nEngineering, Sales, HR, Marketing")

# Question input area
user_question = st.text_input("Ask a question about the employees (e.g., 'Who has the highest salary in Engineering?'):")

if user_question:
    with st.spinner("Analyzing schema and compiling SQL code..."):
        # 1. Translate natural text query to raw SQL statement string 
        generated_sql = generate_clean_sql(user_question)
        
        # Display the SQL code cleanly so the developer/user can inspect it
        st.markdown("##### 💻 Generated SQL Query Syntax:")
        st.code(generated_sql, language="sql")
        
    with st.spinner("Running query against SQLite and parsing results..."):
        # 2. Execute statement directly on local database file data tuples
        db_results, columns = run_sql_query(generated_sql)
        
        # Check if the execution ran into an unexpected database error loop
        if isinstance(db_results, str):
            st.error(f"Execution Error: {db_results}")
        else:
            # 3. Formulate structural textual summarization narrative from row results
            final_answer = generate_final_explanation(user_question, generated_sql, db_results)
            
            st.markdown("##### 🤖 Assistant Answer:")
            st.success(final_answer)
            
            # Optional: Display raw data rows inside an expandable container grid interface
            if db_results:
                with st.expander("Show Raw Database Rows"):
                    st.dataframe(db_results)
