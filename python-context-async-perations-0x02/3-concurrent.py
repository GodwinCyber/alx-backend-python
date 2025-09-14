import aiosqlite
import asyncio
from typing import List, Dict, Any

from user_db import setup_database_concurrent

db_name = 'uses.db'

async def async_fetch_users(db: aiosqlite.Connection) -> List[Dict[str, Any]]:
    '''Fetches all the users from the database'''
    async with db.execute('SELECT name, age FROM users') as cursor:
        rows = await cursor.fetchall()
        print('Fetched all users')
        return [{'name': row[0], 'age': row[1]} for row in rows]
    
async def async_fetch_older_users(db: aiosqlite.Connection) -> List[Dict[str, Any]]:
    '''Fetch users older than 40 from the database'''
    async with db.execute('SELECT name, age FROM users WHERE age > 40;') as cursor:
        rows = await cursor.fetchall()
        print('Fetched older users')
        return [{'name': row[0], 'age': row[1]} for row in rows]
    
async def fetch_concurrently():
    '''Execute both queries concurrently using asyncio.gather.'''
    await setup_database_concurrent(db_name)

    async with aiosqlite.connect(db_name) as db:
        # Run both queries concurrently
        all_users_task = async_fetch_users(db)
        older_users_task = async_fetch_older_users(db)

        # Use asyncio.gather() to execute the coroutines
        all_users, older_users = await asyncio.gather(all_users_task, older_users_task)

        print('\n--- Results from Concurrent Queries ---')

        print('\nAll Users:')
        for user in all_users:
            print(f" - Name: {user['name']}, Age: {user['age']}")

        print('\nUsers Older than 40:')
        for user in older_users:
            print(f" - Name: {user['name']}, Age: {user['age']}")

if __name__ == '__main__':
    asyncio.run(fetch_concurrently())




