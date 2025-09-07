#!/usr/bin/env python3

from mysql.connector import Error
from seed import connect_to_prodev
"""
write a function that uses a generator to fetch rows one by one from the user_data table.
You must use the Yield python generator
    Prototype: def stream_users()
    Your function should have no more than 1 loop
"""

def stream_users():
    query = 'SELECT * FROM user_data'
    connection = connect_to_prodev()
    
    try:
        with connection.cursor(dictionary=True, buffered=True) as cursor:
            cursor.execute(query)
            for row in cursor:
                yield row
    except Error as e:
        print(f"MySQL Error: ", {e})
    finally:
        if connection and connection.is_connected():
            connection.close()

if __name__ == "__main__":
    stream_users()


