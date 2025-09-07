#!/usr/bin/env python3

import csv
import uuid
from mysql.connector import connect, Error

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = ''
DB_NAME = 'ALX_prodev'

def connect_db():
    """Connect to MySQL server without specifying database"""
    try:
        conn = connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD)
        print("Connected to MySQL server")
        return conn
    except Error as e:
        print("DB connection error:", e)
        return None


def create_database(connection):
    """Create ALX_prodev database if it does not exist"""
    query = f'CREATE DATABASE IF NOT EXISTS {DB_NAME}'
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
    except Error as e:
        print(e)


def connect_to_prodev():
    try:
        conn = connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        print("Connected to ALX_prodev database")
        return conn
    except Error as e:
        print("DB connection error:", e)
        return None


def create_table(connection):
    """Create user_data table if it does not exist"""
    query = '''CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(255) PRIMARY KEY, 
                name VARCHAR(255) NOT NULL, 
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL,
                INDEX(user_id)
            )'''
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
            print("Table user_data created successfully")
    except Error as e:
        print(e)


def insert_data(connection, data):
    """Insert CSV rows into user_data table with UUIDs"""
    try:
        with open(data, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            with connection.cursor() as cursor:
                for row in reader:
                    query = '''
                        INSERT IGNORE INTO user_data (user_id, name, email, age)
                        VALUES (%s, %s, %s, %s)
                    '''
                    values = (str(uuid.uuid4()), row['name'], row['email'], row['age'])
                    cursor.execute(query, values)
                connection.commit()
    except Error as e:
        print(f"MySQL Error:", e)
    except FileNotFoundError:
        print(f"CSV file {data} not found")
