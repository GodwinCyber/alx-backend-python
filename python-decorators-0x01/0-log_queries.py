import sqlite3
import functools
import os
from datetime import datetime

from user_db_setup import setup_database_log_queries

#### decorator to lof SQL queries
def log_queries(func):
    """
    create a decorator that logs database queries executed by any function
    Complete the code below by writing a decorator log_queries that logs
    the SQL query before executing it.
        Prototype: def log_queries()
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query', '') if 'query' in kwargs else (args[0] if args else '')
        if query:
            with open('query.log', 'a') as log_file:
                log_file.write(f"{datetime.now()}: Executing query: {query}\n")
        return func(*args, **kwargs)
    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

if __name__ == "__main__":
    ## setup the database
    setup_database_log_queries()

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
for user in users:
    print(user)
