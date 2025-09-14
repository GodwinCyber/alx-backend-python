import aiosqlite
import asyncio
from typing import List, Dict, Any

from user_db import setup_database_concurrent

db_name = 'uses.db'
async def aasync_fetch_users(db: aiosqlite.Connection) -> List[Dict[str, Any]]:
    '''Fetches all the users from the database'''
    async with db.execute('SELECT name, age FROM users') as cursor:
        rows = await cursor.fetchall()
        print('Fetch all users')
        return [{'name': row[0], 'age': row[1]} for row in rows]
    
async def async_fetch_older_users(db: aiosqlite.Connection) -> List[Dict[str, Any]]:
    '''Fetch user older than 40 from the database'''
    async with db.execute('SELECT name, age FROM users WHERE age > 40;') as cursor:
        rows = await cursor.fetchall()
        print('Fetched older user.')
        return [{'name': row[0], 'age': row[1]} for row in rows]
    
async def fetch_concurrently():
    '''Execute both queries concurrently using asyncio.gather.'''
    await setup_database_concurrent(db_name)

    async with aiosqlite.connect(db_name) as db:
        #db.row_factory = aiosqlite.Row # Configure row to be accessible by name

        # Run both queries concurrently
        all_users_task = aasync_fetch_users(db)
        older_users_task = async_fetch_older_users(db)


        # Use asyncio.gather() to execute the coruntines
        all_users, older_users = await asyncio.gather(all_users_task, older_users_task)


        print('\n--- Results from Concurrent Queirs ---')

        print('\n All Users: ')
        for user in all_users:
            print(f' -Name: {user['name']}, Age: {user['age']}')

        print('\n Users Older than 40: ')
        for user in older_users:
            print(f' -Name: {user['name']}, Age: {user['age']}')

if __name__ == '__main__':
    asyncio.run(fetch_concurrently())




