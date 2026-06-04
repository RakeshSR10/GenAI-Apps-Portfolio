import sqlite3

def init_database():
    """Creates a local SQLite database and populates it with sample employee records."""
    # Connects to a local database file (creates it if it doesn't exist)
    connect = sqlite3.connect("employees.db")
    cursor = connect.cursor()

    # Create the Employees table structure
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS EMPLOYEES (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NAME TEXT NOT NULL,
            DEPARTMENT TEXT NOT NULL,
            ROLE TEXT NOT NULL,
            SALARY INTEGER NOT NULL,
            JOIN_DATE TEXT NOT NULL
        )""")
    
    # Check if data already exists to avoid duplicate entries on rerun
    cursor.execute("SELECT COUNT(*) FROM EMPLOYEES")
    if cursor.fetchone()[0] == 0:
        # Sample corporate records
        sample_employees = [
            ('Amit Sharma', 'Engineering', 'Senior Developer', 95000, '2023-01-15'),
            ('Priya Patel', 'Engineering', 'Frontend Engineer', 72000, '2024-03-10'),
            ('Rakesh King', 'Sales', 'Account Executive', 65000, '2022-11-01'),
            ('Sneha Reddy', 'HR', 'HR Manager', 80000, '2021-06-20'),
            ('Vikram Singh', 'Engineering', 'DevOps Specialist', 88000, '2023-08-19'),
            ('Ananya Rao', 'Sales', 'Sales Director', 120000, '2020-02-14'),
            ('Rohan Das', 'Marketing', 'SEO Expert', 55000, '2025-01-10')
        ]

        cursor.executemany("""
            INSERT INTO EMPLOYEES (NAME, DEPARTMENT, ROLE, SALARY, JOIN_DATE) 
            VALUES (?, ?, ?, ?, ?)
        """, sample_employees)
        connect.commit()
    connect.close()

def run_sql_query(query):
    """Executes a generated SQL query safely against the database and returns results."""
    connect = sqlite3.connect("employees.db")
    cursor = connect.cursor()

    try:
        cursor.execute(query)
        results = cursor.fetchall()

        """Executes a generated SQL query safely against the database and returns results."""
        column_names = [description for description in cursor.description]
        connect.close()

        return results, column_names
    
    except Exception as e:
        connect.close()
        return str(e), None
    
if __name__ == "__main__":
    # If run directly, initialize the database for testing
    init_database()
    print("Database 'employees.db' initialized successfully with sample data!")    