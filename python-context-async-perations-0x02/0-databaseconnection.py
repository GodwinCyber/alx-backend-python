import sqlite3
from user_db import setup_database_connection

'''Create a class based context manager to handle opening and closing of a database connection automatically'''

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        print(f'Database connected: {self.db_name}')
        return self.cursor
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f'An exception occured: {exc_val}: transaction rollback.')
            self.connection.rollback()
        else:
            self.connection.commit()
            print(f'Transaction commited')

        self.cursor.close()
        self.connection.close()
        print(f'Database disconnected succesfully')


if __name__ == '__main__':
    ## Connecto the database
    setup_database_connection()
    with DatabaseConnection('users.db') as cursor:
        cursor.execute('SELECT * FROM users')
        result = cursor.fetchall()
        print(f'\nQuery result')
        for row in result:
            print(row)





