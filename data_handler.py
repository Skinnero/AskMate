from connection import CURSOR
from util import catch_all_key_from_table, string_validity_checker

def read_all_data_from_db(table):
    """Takes in a name of a table and returns all contents of it
    as a list of dict

    Args:
        table (str): name of a table

    Returns:
        list: list of dicts
    """    
    CURSOR.execute(f"SELECT * FROM {table} ORDER BY id ASC")
    return CURSOR.fetchall()

def read_single_row_from_db(table,id):
    """Takes in a name of a table and returns single row
    with all of its data

    Args:
        table (str): name of a table

    Returns:
        dict: dicts with data
    """    
    CURSOR.execute(f"SELECT * FROM {table} WHERE id='{id}'")
    return CURSOR.fetchone()

def insert_data_into_db(table,value):
    """Takes is name of a table and value.
    Inserts it to the table

    Args:
        table (str): name of a table
        value (dict): dict for a correct table
    """
    table_keys = catch_all_key_from_table(table)
    value = [v for v in value.values()]
    CURSOR.execute(f"INSERT INTO {table}({','.join(table_keys)}) VALUES ("+"%s"+", %s"*(len(value)-1)+");",value)
    
def delete_data_in_db(table,value):
    """Takes in a name of a table and value.
    Deletes a row with id of a value
    
    Args:
        table (str): name of a table
        value (dict): dict for a correct table
    """    
    CURSOR.execute(f"DELETE FROM {table} WHERE id = '{value['id']}';")
    
def update_data_in_db(table,value):
    """Takes in a name of a table and value.
    Updates every columns by values id.

    Args:
        table (str): name of a table
        value (dict): dict for a correct table
    """    
    for k, v in value.items():
        if v == None:
            continue
        if type(v) == str:
            v = string_validity_checker(v)
        CURSOR.execute(f"UPDATE {table} SET {k} = '{v}' WHERE id = {value['id']}")

def sort_questions_by_order(table,order_by,order_direction):
    """Sorts the table depending on a button urser proviedes

    Args:
        table (str): name of a table
        order_by (str): name of a column
        order_direction (str): direction

    Returns:
        list: list of sorted dicts
    """    
    CURSOR.execute(f"SELECT * FROM {table} ORDER BY {order_by} {order_direction};")
    return CURSOR.fetchall()

def search_database_by_string(text):
    """Looks through db in search for a text
    and returns on inner join question.id = answer.question_id.
    It seraches only by question.title, question.message, answer.message

    Args:
        text (str): search string

    Returns:
        list: list of dicts
    """
    text = text.lower()    
    CURSOR.execute(f"""SELECT DISTINCT question.title, question.submission_time, question.message, question.view_number, question.vote_number
                   FROM question INNER JOIN answer ON question.id=answer.question_id WHERE LOWER(question.title) LIKE '%{text}%'
                   OR LOWER(question.message) LIKE '%{text}%' OR LOWER(answer.message) LIKE '%{text}%'""")
    return CURSOR.fetchall()