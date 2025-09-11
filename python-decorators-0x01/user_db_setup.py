import os
import sqlite3
import uuid

def setup_database_log_queries():
    """Set up a SQLite database with a users table and sample data."""
    db_filename = 'users.db'
    if os.path.exists(db_filename):
        os.remove(db_filename)  # Remove existing database for a fresh setup

    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE users (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    ''')

    # Insert sample data
    users = [
        (str(uuid.uuid4()), 'Alice', 'example@gmail.com'),
        (str(uuid.uuid4()), 'Bob', 'example2@gmail.com'),
        (str(uuid.uuid4()), 'Charlie', 'example3@gm,ail.com')
    ]
    cursor.executemany('INSERT INTO users (id, name, email) VALUES (?, ?, ?)', users)
    conn.commit()
    conn.close()

def setup_database_connection():
    """Set up a SQLite database with a users table and sample data."""
    db_filename = 'users.db'
    if os.path.exists(db_filename):
        os.remove(db_filename)  # Remove existing database for a fresh setup

    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    ''')

    # Insert sample data
    users = [
        ('Alice', 'examle@connection.com'),
        ('Bob', 'example1@connection.com'),
        ('Charlie', 'example2@connection.com'),
        ('David', 'example3@connection.com')
    ]
    cursor.executemany('INSERT INTO users (name, email) VALUES (?, ?)', users)
    conn.commit()
    conn.close()
    print("Database setup complete.")

def setup_database_transactions():
    """Set up a SQLite database with a users table and sample data."""
    db_filename = 'users.db'
    if os.path.exists(db_filename):
        os.remove(db_filename)  # Remove existing database for a fresh setup

    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    ''')

    # Insert sample data
    users = [
        ('Alice', 'example@transaction.com'),
        ('Bob', 'example1@transaction.com'),
        ('Charlie', 'example2@transaction.com'),
        ('David', 'example3@transaction.com')
    ]
    cursor.executemany('INSERT INTO users (name, email) VALUES (?, ?)', users)
    conn.commit()
    conn.close()
    print("Database setup complete.")


def setup_database_retry():
    """Set up a SQLite database with a users table and sample data."""
    db_filename = 'users.db'
    if os.path.exists(db_filename):
        os.remove(db_filename)  # Remove existing database for a fresh setup

    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE users (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    ''')

    # Insert sample data
    users = [
        (str(uuid.uuid4()), 'Alice', 'example@setup.com'),
        (str(uuid.uuid4()), 'Bob', 'example1@setup.com'),
        (str(uuid.uuid4()), 'Charlie', 'example2@setup.com'),
        (str(uuid.uuid4()), 'David', 'example3@setup.com')
    ]
    cursor.executemany('INSERT INTO users (id, name, email) VALUES (?, ?, ?)', users)
    conn.commit()
    conn.close()
    print("Database setup complete.")

