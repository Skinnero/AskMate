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
    
def prepare_answer_before_saving(data):
    """Prepares data for saving
    (Only for answer)

    Args:
        data (dict): dict of changed data

    Returns:
        dict: prepared data to change
    """    
    return {
            'submission_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
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
            'submission_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'view_number': 0,
            'vote_number': 0,
            'title': data['title'],
            'message': data['message'],
            'image': data.get('image',''),
                }

def prepare_comment_before_saving(data):
    """Prepares data for saving
    (Only for comment)

    Args:
        data (dict): dict of changed data

    Returns:
        dict: prepared data to change
    """
    return {
            'question_id': data.get('question_id'),
            'answer_id': data.get('answer_id'),
            'message': data['message'],
            'submission_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'edited_count': 0,
                }

def string_validity_checker(text):
    """Takes the string and prepares it for
    saving into db

    Args:
        text (str): string 

    Returns:
        str: valid string
    """    
    return text.replace("'", "''")

