import psycopg2
from psycopg2.extras import RealDictCursor
from os import path, environ
from dotenv import load_dotenv

# Load .env
load_dotenv()

# DB Table names
ANSWER = 'answer'
QUESTION = 'question'
COMMENT = 'comment'
TAG = 'tag'
QUESTION_TAG = 'question_tag'
USERS = 'users'

# Image folder
IMAGE_DATA = path.join('static', 'images')
ALLOWED_EXTENSIONS = {'txt','jpg','png','jpeg'}

# Enviroment data
DATABASE = environ.get('DATABASE')
DB_USER = environ.get('USER')
PASSWORD = environ.get('PASSWORD')

def connect_to_database():
    """Conncts to database and returns cursor

    Returns:
        class: cursor 
    """
    try:
        with psycopg2.connect(database=DATABASE, user=DB_USER, password=PASSWORD) as conn:
            conn.autocommit = True
            return conn.cursor(cursor_factory=RealDictCursor)
    except psycopg2.DatabaseError as exception:
        print('Database connection problem')
        raise exception

# Assign cursor to constant variable
CURSOR = connect_to_database()
