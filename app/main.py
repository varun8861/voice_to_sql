# app/main.py

from .transcription import get_transcript_from_text
from .text_to_sql import generate_sql_query
from .database import setup_database, execute_read_query # <-- Updated import

def main():
    """
    Main function to run the Voice-to-SQL application.
    """
    setup_database()

    # Let's use a query that will return data from our dummy tables
    user_query = "List the first name and email of all customers"
    print(f"\nUser Input: '{user_query}'")

    transcribed_text = get_transcript_from_text(user_query)
    sql_query = generate_sql_query(transcribed_text)
    
    print("\n--------------------------")
    print("✅ Generated SQL Query:")
    print(sql_query)
    print("--------------------------\n")

    # 4. Execute the query and get results
    headers, results = execute_read_query(sql_query)

    # 5. Display the results
    if results:
        # Print headers
        print("✅ Query Results:")
        print(" | ".join(headers))
        print("-" * (len(" | ".join(headers)))) # Dynamic separator

        # Print rows
        for row in results:
            print(" | ".join(str(value) for value in row))
    elif headers:
         # This handles cases where there's an error message in the headers
         print(f"❌ {headers[0]}")
    else:
        print("✅ Query executed successfully, but returned no results.")


if __name__ == "__main__":
    main()