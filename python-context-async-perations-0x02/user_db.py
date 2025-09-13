import os
import sqlite3
import uuid

def setup_database_connection():
    '''set up a SQLite database with a users table and sample data'''
    db_filename = 'users.db'
    if os.path.exists(db_filename):
        os.remove(db_filename)  # Remove existing database for a fresh setup
    conn = sqlite3.connect(db_filename) # Create a new database connection
    cursor = conn.cursor() # Create a cursor object to execute SQL commands
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    ''')

    # Insert sample data
    user_id = [
        (str(uuid.uuid4()), 'Alice', 'example@alice.com'),
        (str(uuid.uuid4()), 'Bob', 'example@bob.com'),
        (str(uuid.uuid4()), 'Charlie', 'example@charlie.com')
    ]
    cursor.executemany('INSERT INTO users (id, name, email) VALUES (?, ?, ?)', user_id)
    conn.commit()
    conn.close()
    print("Database setup complete.")

