import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv()

def verify_db_connection():
    """Test the database connection and print diagnostic information"""
    try:
        connection = get_db_connection()
        if connection and connection.is_connected():
            db_info = connection.get_server_info()
            print(f"Connected to MySQL Server version {db_info}")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print(f"You're connected to database: {record[0]}")
            
            # Test a simple query to ensure tables exist
            try:
                cursor.execute("SHOW TABLES;")
                tables = cursor.fetchall()
                print(f"Available tables: {[table[0] for table in tables]}")
                if not tables:
                    print("WARNING: No tables found in the database!")
            except Error as e:
                print(f"Error testing tables: {e}")
                
            cursor.close()
            connection.close()
            return True
        else:
            print("Failed to connect to database!")
            return False
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        print(f"DB_HOST: {os.getenv('DB_HOST')}")
        print(f"DB_PORT: {os.getenv('DB_PORT')}")
        print(f"DB_USER: {os.getenv('DB_USER')}")
        print(f"DB_NAME: {os.getenv('DB_NAME')}")
        print("DB_PASSWORD: [HIDDEN]")
        return False

def get_db_connection():
    """Create a connection to the MySQL database"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

def execute_query(connection, query, params=None):
    """Execute a query on the database"""
    cursor = connection.cursor(dictionary=True)
    try:
        if params:
            print(f"Executing query with params: {query} {params}")  # Debug log
            cursor.execute(query, params)
        else:
            print(f"Executing query: {query}")  # Debug log
            cursor.execute(query)
        
        if query.strip().upper().startswith(('SELECT', 'SHOW')):
            result = cursor.fetchall()
            return result
        else:
            connection.commit()
            return cursor.lastrowid
    except Error as e:
        print(f"Error executing query: {e}")
        print(f"Query: {query}")
        print(f"Params: {params}")
        connection.rollback()  # Rollback the transaction on error
        raise  # Re-raise the exception to be caught by the calling function
    finally:
        cursor.close()

# If this script is run directly, verify the database connection
if __name__ == "__main__":
    if verify_db_connection():
        print("Database connection successful!")
        sys.exit(0)
    else:
        print("Database connection failed!")
        sys.exit(1) 