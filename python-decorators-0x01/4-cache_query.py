import os
from datetime import datetime
import sqlite3
import functools

from user_db_setup import setup_database_cache
from with_db_connection import with_db_connection

# Decorator to cache query results
def cache_query(func):
    """
    Create a decorator that caches the results of database queries to avoid redundant database hits.
    The decorator should:
        - Store the results of the function in a cache (e.g., a dictionary) with the query parameters as the key.
        - Return the cached result if the same query parameters are used again.
        - Ensure that the cache is specific to each decorated function.
    Prototype: def cache_query(func)
    """
    query_cache = {}

    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        if query in query_cache:
            print(f"Fetching result from cache for query: {query}")
            return query_cache[query]

        result = func(conn, query, *args, **kwargs)
        query_cache[query] = result
        print(f"Caching result for query: {query}")
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

if __name__ == "__main__":
    ## setup the database
    setup_database_cache()

    #### First call will cache the result
    users = fetch_users_with_cache(query="SELECT * FROM users")
    

    #### Second call will use the cached result
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
