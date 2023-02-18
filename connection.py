from csv import DictReader, DictWriter
from os import path

QUESTION_DATA = "sample_data/question.csv"
ANSWER_DATA = "sample_data/answer.csv"
IMAGE_DATA = path.join('static','images')

def read_csv_file(filename):
    """Read file and puts it to list as a list of dict

    Args:
        filename (str): path to the file

    Returns:
        list: list of dict
    """    
    with open (filename, encoding="utf-8") as csv_file:
        csv_read_dict = DictReader(csv_file)
        list_of_dict = []
        for row in csv_read_dict:
            list_of_dict.append(row)
        return list_of_dict

def get_field_names_from_csv(filename):
    """Return field names from csv file

    Args:
        filename (str): path to the file

    Returns:
        list: list of field names
    """    
    with open (filename, encoding="utf-8") as csv_file:
        csv_read_dict = DictReader(csv_file)
        return csv_read_dict.fieldnames           
            
def write_to_csv_file(filename,file_data):
    """Opens file and writes file_data to it

    Args:
        filename (str): path to the file
        data (dict): keys and values from answers/questions
    """    
    
    field_names = get_field_names_from_csv(filename)
    with open (filename, 'w', newline='', encoding="utf-8") as csv_file:
        csv_write_dict = DictWriter(csv_file, fieldnames=field_names)
        csv_write_dict.writeheader()
        csv_write_dict.writerows(file_data)
