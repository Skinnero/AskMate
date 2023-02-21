from connection import CURSOR
from datetime import datetime

def catch_all_key_from_table(table):
    """Takes in a table name and returns all column names
    in a list

    Args:
        table (str): name of a table

    Returns:
        list: list of column names
    """    
    CURSOR.execute(f'SELECT * FROM {table}')
    return [k for k in CURSOR.fetchone().keys() if k != 'id']
    
def get_data_by_id(id,list_of_data):
    """Takes in id and list of data and iterates
    through them in search for specific id.

    Args:
        id (str): id of a data
        list_of_data (list): list of dicts of a data
    """
    for d in list_of_data:
        if int(d['id']) == int(id):
            return d    
        
def prepare_answer_before_saving(data):
    """Prepares data for saving
    (Only for answer)

    Args:
        data (dict): dict of changed data

    Returns:
        dict: prepared data to change
    """    
    return {
            'submission_time': datetime.now(),
            'vote_number': 0,
            'question_id': data['question_id'],
            'message': data['message'],
            'image': data['image'],
                }
    
def prepare_question_before_saving(data):
    """Prepares data for saving
    (Only for question)

    Args:
        data (dict): dict of changed data

    Returns:
        dict: prepared data to change
    """
    return {
            'submission_time': datetime.now(),
            'view_number': 0,
            'vote_number': 0,
            'title': data['title'],
            'message': data['message'],
            'image': data['image'],
                }

