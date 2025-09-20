# app/server.py

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated

# Import our backend functions
from .text_to_sql import generate_sql_query
from .database import execute_read_query, setup_database

# Create the FastAPI app object
app = FastAPI()

# Point to the 'templates' directory
templates = Jinja2Templates(directory="app/templates")

@app.on_event("startup")
def on_startup():
    """
    This function runs when the server starts.
    We'll use it to set up the database.
    """
    print("Server is starting up...")
    setup_database()
    print("Database setup complete.")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    This function handles the initial page load (GET request).
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/process-query", response_class=HTMLResponse)
async def process_query(request: Request, query: Annotated[str, Form()]):
    """
    This function handles the form submission (POST request).
    It calls the Gemini API, executes the SQL, and returns the results.
    """
    print(f"Received query from form: {query}")

    # 1. Generate SQL from the natural language query
    generated_sql = generate_sql_query(query)
    
    # 2. Execute the SQL query on the database
    headers, results = execute_read_query(generated_sql)

    # 3. Pass all the data to the template
    context = {
        "request": request,
        "user_query": query,
        "generated_sql": generated_sql,
        "results_headers": headers,
        "query_results": results
    }
    # This line is the most important part!
    return templates.TemplateResponse("index.html", context)