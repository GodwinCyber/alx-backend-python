import sqlite3
from user_db import setup_database_execute


class ExecuteQuery:
    '''''reate a resuable context manager that take query as input and execute it, managing both connevction and query execution'''
    def __init__(self, db_path, query, params=None):
        self.db_path = db_path
        self.query = query
        self.params = params or ()
        self.connection = None
        self.cursor = None

    def __enter__(self):
        '''Establishes a connection to db and cretae cursor:
        Return:
            list: the result of the executed query
        '''
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
            self.cursor.execute(self.query, self.params)
            return self.cursor.fetchall()
        except sqlite3.DatabaseError as e:
            if self.connection:
                self.connection.rollback()
            raise e


    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            if exc_type is None:
                self.connection.commit()
            self.connection.close()

if __name__ == '__main__':
    db_path = 'user_db'
    
    ## Database connection
    setup_database_execute(db_path)

    query = 'SELECT * FROM users WHERE age > ?'
    params = (25,)

    with ExecuteQuery(db_path, query, params) as result:
        for row in result:
            print('Query result', result)









