from connection import CURSOR
from util import catch_all_key_from_table

def read_all_data_from_db(table):
    """Takes in a name of a table and returns all contents of it
    as a list of dict

    Args:
        table (str): name of a table

    Returns:
        list: list of dicts
    """    
    CURSOR.execute(f"SELECT * FROM {table}")
    return CURSOR.fetchall()

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
