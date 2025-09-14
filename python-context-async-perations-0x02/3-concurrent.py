#!/usr/bin/env python3
"""
Concurrent fetching of users using aiosqlite.
Includes two coroutines:
- async_fetch_users(): fetches all users
- async_fetch_older_users(): fetches users older than 40
"""

import aiosqlite
import asyncio
from typing import List, Dict, Any
from user_db import setup_database_concurrent

db_name = 'uses.db'


async def async_fetch_users(db: aiosqlite.Connection) -> List[Dict[str, Any]]:
    """Fetches all the users from the database"""
    async with db.execute("SELECT name, age FROM users;") as cursor:
        rows = await cursor.fetchall()
        return [{'name': row[0], 'age': row[1]} for row in rows]


async def async_fetch_older_users(db: aiosqlite.Connection) -> List[Dict[str, Any]]:
    """Fetch users older than 40 from the database"""
    async with db.execute("SELECT name, age FROM users WHERE age > 40;") as cursor:
        rows = await cursor.fetchall()
        return [{'name': row[0], 'age': row[1]} for row in rows]


async def fetch_concurrently():
    """Execute both queries concurrently using asyncio.gather."""
    await setup_database_concurrent(db_name)

    async with aiosqlite.connect(db_name) as db:
        # Run both queries concurrently
        all_users, older_users = await asyncio.gather(
            async_fetch_users(db),
            async_fetch_older_users(db)
        )

        print("\nAll Users:")
        for user in all_users:
            print(f"{user['name']} - {user['age']}")

        print("\nUsers Older than 40:")
        for user in older_users:
            print(f"{user['name']} - {user['age']}")


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())





