#!/bin/usr/env python3
"""You are not allowed to use the SQL AVERAGE task"""

from mysql.connector import Error
seed = __import__('seed')

"""
Implement a generator stream_user_ages() that yields user ages one by one.

Use the generator in a different function to calculate the average age without loading the entire dataset into memory

Your script should print Average age of users: average age

You must use no more than two loops in your script

You are not allowed to use the SQL AVERAGE
    Prototype: def stream_user_ages()
"""

def stream_user_ages():
    query = 'SELECT age FROM user_data'
    connection = seed.connect_to_prodev()
    
    try:
        with connection.cursor(dictionary=True, buffered=True) as cursor:
            cursor.execute(query)
            for row in cursor:
                yield row.get('age', 0)
    except Error as e:
        print(f"MySQL Error: ", {e})
    finally:
        if connection and connection.is_connected():
            connection.close()
    return

if __name__ == "__main__":
    total_age = 0
    count = 0
    for age in stream_user_ages():
        total_age += age
        count += 1
    average_age = total_age / count if count > 0 else 0
    print(f"Average age of users: {average_age}")
