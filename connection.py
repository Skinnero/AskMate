import psycopg2
from psycopg2.extras import RealDictCursor
from os import path
from enviroment import DATABASE, USER, PASSWORD


# DB Table names
ANSWER = 'answer'
QUESTION = 'question'
COMMENT = 'comment'
TAG = 'tag'
QUESTION_TAG = 'question_tag'

# Image folder
IMAGE_DATA = path.join('static','images')

def connect_to_database():
    """Conncts to database and returns cursor

    Returns:
        class: cursor 
    """
    try:
        with psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD) as conn:
            conn.autocommit = True
            return conn.cursor(cursor_factory=RealDictCursor)
    except psycopg2.DatabaseError as exception:
        print('Database connection problem')
        raise exception

# Assign cursor to constant variable
CURSOR = connect_to_database()
