import os
from datetime import datetime
import sqlite3
import functools

from user_db_setup import setup_database_connection

#### decorator to manage DB connection
def with_db_connection(func):
    """
    Create a decorator that manages the database connection for any function.
    The decorator should:
        - Establish a connection to the SQLite database before executing the function.
        - Pass the database connection as the first argument to the decorated function.
        - Ensure the connection is properly closed after the function execution, even if an error occurs.
    Prototype: def with_db_connection()
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper



@with_db_connection 
def get_user_by_id(conn, user_id): 
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)) 
    return cursor.fetchone() 
#### Fetch user by ID with automatic connection handling 


if __name__ == "__main__":
    ## setup the database
    setup_database_connection()
    user = get_user_by_id(user_id=3)
    print("User with ID 1:", user)
