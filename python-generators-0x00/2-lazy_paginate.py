#!/usr/bin/env python3

seed = __import__('seed')

"""
Lazy pagination generator
Implement a generator function lazypaginate(pagesize) that implements the
paginate_users(page_size, offset) that will only fetch the next page when needed at an offset of 0.
    You must only use one loop
    Include the paginate_users function in your code
    You must use the yield generator
    Prototype:
    def lazy_paginate(page_size)
"""

def paginate_users(page_size, offset):
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f'SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}')
    rows = cursor.fetchall()
    cursor.close()
    return rows

def lazy_paginate(page_size):
    offset = 0
    while True:
        rows = paginate_users(page_size, offset)
        if not rows:
            break
        yield rows
        offset += page_size
    return None

if __name__ == "__main__":
    for page in lazy_paginate(10):
        for user in page:
            print(user)



