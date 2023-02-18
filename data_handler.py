import time
from connection import read_csv_file, write_to_csv_file

def sort_table(order_by, order_direction, table):
    """Sorts the table by numbers or alphabeticly

    Args:
        order_by (str): string of the key
        order_direction (str): desc or asc
        table (list): list of dicts of questions

    Returns:
        list: sorted list of dicts
    """    
    reverse = False
    if order_direction == 'asc':
        reverse = True
    table = sorted(table,key=lambda k:check_for_type(k,order_by), reverse=reverse)
    return table

def check_for_type(k,order_by):
    """Return int or str depending of a value of a given key

    Args:
        k (dict): given dict
        order_by (str): name of a key

    Returns:
        int or str: depends if a value can be converted to int otherwise it's string
    """    
    try:
        return int(k[order_by])
    except:
        return str(k[order_by])

def delete_data_from_file(filename, data):
    """Opens the file and then removes data from it

    Args:
        filename (str): name of file
        data (dict): data of question/answer
    """    
    file_data = read_csv_file(filename)
    file_data.remove(data)
    write_to_csv_file(filename,file_data)

def delete_answers_to_question(filename,question_id):
    """Takes question_id and deletes all answer to that question

    Args:
        filename (str): name of a file
        question_id (str): question id
    """    
    file_data = read_csv_file(filename)
    updated_data = [answer for answer in file_data if answer['question_id'] != question_id]
    write_to_csv_file(filename,updated_data)

def adding_to_file(filename, data):
    """Opens the file and saves data to it

    Args:
        filename (str): name of file
        data (dict): data of question/answer
    """
    file_data = read_csv_file(filename)
    if 'question' in filename:
        new_data = {
            'id': len(file_data)+1,
            'submission_time': int(time.time()),
            'view_number': 0,
            'vote_number': 0,
            'title': data['title'],
            'message': data['message'],
            'image': data['image'],
                    }
    elif 'answer' in filename:
        new_data = {
        'id': len(file_data)+1,
        'submission_time': int(time.time()),
        'vote_number': 0,
        'question_id': data['question_id'],
        'message': data['message'],
        'image': data['image'],
                }
    file_data.append(new_data)
    manage_id_data(filename)
    write_to_csv_file(filename,file_data)

def edit_data(filename, web_data, data):
    """Takes in the web_data and data, takes its ID from
    file_data and changes values of data's keys

    Args:
        filename (str): name of a file
        web_data (dict): data from website to change
        data (dict): data of a question/answer
    """    
    file_data = read_csv_file(filename)
    data_index = file_data.index(data)
    for key in web_data.keys():
        if key in file_data[data_index].keys():
            file_data[data_index][key] = web_data[key]
    write_to_csv_file(filename, file_data)
    
def manage_id_data(filename):
    """Check if the id's are in order if not puts them likewise

    Args:
        filename (str): name of a file
    """    
    file_data = read_csv_file(filename)
    for i in range(len(file_data)):
        if file_data[i]['id'] != str(i+1):
            file_data[i]['id'] = i+1
    write_to_csv_file(filename, file_data)