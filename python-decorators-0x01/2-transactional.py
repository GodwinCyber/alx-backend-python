import os
from datetime import datetime
import sqlite3
import functools

from user_db_setup import setup_database_transactions

#### decorator to manage DB transactions

def with_db_connection(func):
    """Open SQlLite Connection, passes it into the function, and ensure it closed"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

def transactional(func):
    """
    Create a decorator that manages database transactions for any function.
    The decorator should:
        - Begin a transaction before executing the function.
        - Commit the transaction if the function executes successfully.
        - Roll back the transaction if an exception occurs during function execution.
        - Ensure the database connection is properly closed after the function execution, regardless of success or failure.
    Prototype: def transactional(func)
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            conn.execute('BEGIN')
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            print(f"Transaction failed: {e}")
            raise
        finally:
            conn.close()
    return wrapper


@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 

@with_db_connection
def get_user_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

if __name__ == "__main__":
    ## setup the database
    setup_database_transactions()
    #### Update user's email with automatic transaction handling 

update_user_email(1, 'Crawford_Cartwright@hotmail.com')
print("User email updated successfully.")
update_user_email(2, 'Crawford1_Cartwright@hotmail.com')
user = get_user_id(1)
print("User with ID 1:", user)
user = get_user_id(2)
print("User with ID 2:", user)
