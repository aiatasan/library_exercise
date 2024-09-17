'''
Library Management API using FastAPI and SQLite
'''

# Setting up the SQLite database

import sqlite3


def init_db():
    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS authors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author_id INTEGER,
        published_date DATE,
        FOREIGN KEY (author_id) REFERENCES authors (id)
    )
    ''')

    connection.commit()
    connection.close()
