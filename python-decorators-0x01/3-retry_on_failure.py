import os
from datetime import datetime
import sqlite3
import functools
import time

from user_db_setup import setup_database_retry

def with_db_connection(func):
    """Open SQLite Connection, passes it into the function, and ensure it closed"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper
def retry_on_failure(retries=3, delay=2):
    """
    Retry a database operation on failure of a transient error.
    Decorator that retries the function of a certain number of times if it raises an exception
    Args:
        retries (int): Number of retry attempts.
        delay (int): Delay in seconds between retries.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except sqlite3.OperationalError as e:
                    last_exception = e
                    print(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay} deconds...")
                    time.sleep(delay)
            print("All retry attempts failed.")
            raise last_exception
        return wrapper
    return decorator



@with_db_connection
@retry_on_failure(retries=3, delay=1)

def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

if __name__ == "__main__":
    ## setup the database
    setup_database_retry()

    #### attempt to fetch users with automatic retry on failure
    users = fetch_users_with_retry()
    for user in users:
        print(user)
