# app/text_to_sql.py

import os 
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Please set it in the .env file.")
genai.configure(api_key=api_key)



def generate_sql_query(natural_language_query: str) -> str:
    """
    Generates an SQL query from a natural language query using the Gemini API.
    """
    # For now, we hardcode the schema. Later, we can generate this dynamically.
    db_schema = """
    CREATE TABLE customers (
        id INTEGER PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        email TEXT,
        join_date TEXT
    );
    CREATE TABLE products (
        id INTEGER PRIMARY KEY,
        name TEXT,
        price REAL,
        stock INTEGER
    );
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        product_id INTEGER,
        order_date TEXT,
        quantity INTEGER
    );
    """

    # This is our "prompt engineering". We give the AI its role, context, and the task.
    prompt = f"""
    You are an expert SQLite programmer. Your task is to write SQL queries based on natural language questions.
    You will be given a question and the database schema.
    Your response must be ONLY the SQL query, with no other text, explanation, or markdown.

    Here is the database schema:
    {db_schema}

    Here is the user's question:
    "{natural_language_query}"

    Generated SQL Query:
    """

    print("🤖 Calling Gemini API to generate SQL...")
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(prompt)
        
        # Clean up the response to get only the SQL
        sql_query = response.text.strip()
        # Sometimes the model wraps the SQL in markdown, so we remove it.
        if sql_query.startswith("```sql"):
            sql_query = sql_query[6:]
        if sql_query.endswith("```"):
            sql_query = sql_query[:-3]
        
        return sql_query.strip()
        
    except Exception as e:
        print(f"❌ An error occurred with the Gemini API: {e}")
        return "SELECT 'An error occurred while generating SQL' AS Error;"
