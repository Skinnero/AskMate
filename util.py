from connection import read_csv_file, write_to_csv_file

def get_data_by_id(id,file):
    """Searches through the file for id and returns it as dict

    Args:
        id (str): id of a question that user picked
        file (list): list of dict from file

    Returns:
        dict: dict with corresponding id
    """    
    list_of_id = read_csv_file(file)
    for row in list_of_id:
        if row['id'] == id:
            return row

def vote_changer(filename, data, decision):
    """Takes is the data and iterates through file_data
    if encounter data the changes its value depending of
    the decision

    Args:
        data (dict): data of a question/answer
        decision (bool): True if +1, False if -1

    Returns:
        dict: changed data
    """
    file_data = read_csv_file(filename)    
    for dictionary in file_data:
        if dictionary == data and decision == True:
            dictionary['vote_number'] = int(dictionary['vote_number']) + 1
            write_to_csv_file(filename, file_data)
        elif dictionary == data and decision == False:
            dictionary['vote_number'] = int(dictionary['vote_number']) - 1
            write_to_csv_file(filename, file_data)
            
def question_view_number_changer(filename, data):
    
    file_data = read_csv_file(filename)
    for question in file_data:
        if question == data:
            question['view_number'] = int(question['view_number']) + 1
    write_to_csv_file(filename, file_data)