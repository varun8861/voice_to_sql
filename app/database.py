# app/database.py

import sqlite3
import os

# Define the path for the database file in the project's root directory
# os.path.join(os.path.dirname(__file__), '..', 'database.db')
# This navigates one level up from the 'app' directory to the project root
DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'database.db')


def create_connection():
    """Create a database connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        print(f"✅ Successfully connected to SQLite database at {DB_FILE}")
    except sqlite3.Error as e:
        print(f"❌ Error connecting to database: {e}")
    return conn


def execute_sql(conn, sql_statement):
    """Execute a single SQL statement."""
    try:
        c = conn.cursor()
        c.execute(sql_statement)
    except sqlite3.Error as e:
        print(f"❌ Error executing SQL: {e}")


def setup_database():
    """Create database tables and insert dummy data."""

    # SQL statements to create our tables
    # We use """ for multi-line strings
    create_customers_table = """
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        join_date TEXT NOT NULL
    );
    """

    create_products_table = """
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        stock INTEGER NOT NULL
    );
    """

    create_orders_table = """
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        order_date TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers (id),
        FOREIGN KEY (product_id) REFERENCES products (id)
    );
    """

    # SQL statements to insert dummy data
    # 'INSERT OR IGNORE' will prevent errors if we run this script multiple times
    insert_customers = """
    INSERT OR IGNORE INTO customers (id, first_name, last_name, email, join_date) VALUES
    (1, 'John', 'Doe', 'john.doe@email.com', '2023-01-15'),
    (2, 'Jane', 'Smith', 'jane.smith@email.com', '2023-03-20'),
    (3, 'Peter', 'Jones', 'peter.jones@email.com', '2023-05-30');
    """

    insert_products = """
    INSERT OR IGNORE INTO products (id, name, price, stock) VALUES
    (1, 'Laptop', 1200.50, 50),
    (2, 'Mouse', 25.00, 200),
    (3, 'Keyboard', 75.99, 150);
    """

    insert_orders = """
    INSERT OR IGNORE INTO orders (id, customer_id, product_id, order_date, quantity) VALUES
    (1, 1, 1, '2024-02-10', 1),
    (2, 2, 3, '2024-04-05', 2),
    (3, 1, 2, '2024-05-21', 3);
    """
    
    conn = create_connection()

    if conn is not None:
        # Create tables
        print("\nCreating tables...")
        execute_sql(conn, create_customers_table)
        execute_sql(conn, create_products_table)
        execute_sql(conn, create_orders_table)
        print("✅ Tables created successfully (or already exist).")

        # Insert dummy data
        print("\nInserting dummy data...")
        execute_sql(conn, insert_customers)
        execute_sql(conn, insert_products)
        execute_sql(conn, insert_orders)
        print("✅ Dummy data inserted successfully (or already exists).")
        
        # Commit the changes and close the connection
        conn.commit()
        conn.close()
        print("\nDatabase setup complete and connection closed.")
    else:
        print("❌ Could not create database connection.")
        
        
        
def execute_read_query(sql_query: str):
    """Executes a read query and returns the results."""
    conn = create_connection()
    if conn is None:
        return [], []

    # This makes the output of fetchall() a list of dictionary-like Row objects
    # which lets us access columns by name.
    conn.row_factory = sqlite3.Row 
    
    try:
        cursor = conn.cursor()
        cursor.execute(sql_query)
        results = cursor.fetchall()
        # Get column headers from the cursor description
        headers = [description[0] for description in cursor.description]
        return headers, results
    except sqlite3.Error as e:
        print(f"❌ Error executing read query: {e}")
        return [f"Error: {e}"], []
    finally:
        if conn:
            conn.close()

# This allows us to run this file directly for testing if needed
if __name__ == '__main__':
    setup_database()