#!/usr/bin/env python3

"""
Write a function that stream user in batches (batch size) that fetch row in batches
write a function that process each batch to filter user over the age of 25
you must not used more than 3 loops in the code
the script must use yield generator
prototype: 
        def stream_users_in_batches(batch_size)
        def batch_processing(batch_size)
"""

from seed import connect_to_prodev
from mysql.connector import Error

def stream_users_in_batches(batch_size):
    query = 'SELECT * FROM user_data'
    connection = connect_to_prodev()
    
    try:
        with connection.cursor(dictionary=True, buffered=True) as cursor:
            cursor.execute(query)
            while True:
                batch = cursor.fetchmany(batch_size)
                if not batch:
                    break
                yield batch
    except Error as e:
        print(f"MySQL Error: ", {e})
    finally:
        if connection and connection.is_connected():
            connection.close()
    return

def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        if not batch:
            print("No batch found")
        for user in batch:
            if user.get('age', 0) > 25:
                yield user
    return

if __name__ == "__main__":
    for user in batch_processing(10):
        print(user)

