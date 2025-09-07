__Objective:__ create a generator that streams rows from an SQL database one by one.
__Instructions:__

Write a python script that seed.py:

-    Set up the MySQL database, ALX_prodev with the table user_data with the following fields:
-    user_id(Primary Key, UUID, Indexed)
-    name (VARCHAR, NOT NULL)
-    email (VARCHAR, NOT NULL)
-    age (DECIMAL,NOT NULL)
-    Populate the database with the sample data from this user_data.csv
-    Prototypes:
-    def connect_db() :- connects to the mysql database server
-    def create_database(connection):- creates the database ALX_prodev if it does not exist
-    def connect_to_prodev() connects the the ALX_prodev database in MYSQL
-    def create_table(connection):- creates a table user_data if it does not exists with the required fields
-    def insert_data(connection, data):- inserts data in the database if it does not exist


```python
#!/usr/bin/python3

seed = __import__('seed')

connection = seed.connect_db()
if connection:
    seed.create_database(connection)
    connection.close()
    print(f"connection successful")

    connection = seed.connect_to_prodev()

    if connection:
        seed.create_table(connection)
        seed.insert_data(connection, 'user_data.csv')
        cursor = connection.cursor()
        cursor.execute(f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'ALX_prodev';")
        result = cursor.fetchone()
        if result:
            print(f"Database ALX_prodev is present ")
        cursor.execute(f"SELECT * FROM user_data LIMIT 5;")
        rows = cursor.fetchall()
        print(rows)
        cursor.close()
```
