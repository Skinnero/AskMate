from datetime import datetime
from werkzeug.utils import secure_filename
from connection import IMAGE_DATA, ALLOWED_EXTENSIONS
from os import path
import bcrypt


def prepare_user_before_saving(data):
    """Prepares data for saving
    (Only for user)

    Args:
        data (dict): dict of changed data

    Returns:
        dict: prepared data to change
    """
    return {
        'user_name': data['user_name'],
        'email': data['user_email'],
        'password': data['user_password'],
        'reputation': 0,
    }


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
        'user_id': data['user_id']
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
        'image': data.get('image', ''),
        'user_id': data['user_id']
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
        'user_id': data['user_id']
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


def adding_valid_image_path(image_name: str):
    """Takes in an image name and checks if
    it contains something, if yes, then saves it
    onto server and returns it's string

    Args:
        image_name (str): name of a file from request

    Returns:
        str: secure filename
    """
    if image_name.filename != '' and check_for_valid_extensions(image_name.filename):
        secure_image_name = secure_filename(image_name.filename)
        image_name.save(path.join(IMAGE_DATA, secure_image_name))
        return secure_image_name
    return image_name.filename


def check_for_valid_extensions(image_name):
    """Checks if extension is allowed

    Args:
        image_name (str): name of a file

    Returns:
        bool: True if is allowed else False
    """
    return '.' in image_name and image_name.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def create_password(password):
    """Generate hashed password and returns it

    Args:
        password (str): str of user input

    Returns:
        str: str of password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password, hashed_password):

    return bcrypt.checkpw(password, hashed_password)
