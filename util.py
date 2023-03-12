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
        'submission_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'reputation': 0,
    }


def prepare_user_vote_before_saving(user_id, voted, **text_id):
    """Prepares data for saving
    (Only for user_vote)

    Args:
        user_id (int): user id
        text_id (kwargs): kwargs 'question_id' or 'answer_id' 
        voted (int): 1 for upvote otherwise -1

    Returns:
        dict: prepare data to change
    """
    return {
        'user_id': user_id,
        'voted': voted,
        'question_id': text_id.get('question_id', None),
        'answer_id': text_id.get('answer_id', None)
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
        'user_id': data['user_id'],
        'accepted': 0
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
    """Takes in user password, and hashed password from db
    abd checks it if it's the same

    Args:
        password (str): already encoded string
        hashed_password (str): already encoded string

    Returns:
        bool: True if it's the same otherwise False
    """
    return bcrypt.checkpw(password, hashed_password)


def calculate_user_reputation(data):
    """Calculate all votes from tables and puts it into 
    the 'reputation' key

    Args:
        data (list): list of dicts

    Returns:
        data: list of dicts 
    """
    for user in data:
        user['question_vote_up'] *= 5
        user['question_vote_down'] *= 2
        user['answer_vote_up'] *= 10
        user['answer_vote_down'] *= 2
        user['answer_accepted'] *= 15
        user['reputation'] = sum(
            [v for k, v in user.items() if k != 'user_name'])
        user.pop('question_vote_up')
        user.pop('question_vote_down')
        user.pop('answer_vote_up')
        user.pop('answer_vote_down')
        user.pop('answer_accepted')
    return data


def divide_vote_data(data_to_seperate, data, user_id, data_id):
    """Divides vote date so it can be easily printed for question
    as well as for answers

    Args:
        data_to_seperate (str): 'question' or 'answer'
        data (list): list of users_vote
        user_id (int): session user id
        data_id (list or int): list for answers as a whole RealDictReader 
        or int for question as a question id
    Returns:
        list: divided list 
    """
    if data_to_seperate == 'question':
        try:
            return [q for q in data if q['user_id'] == user_id and q['question_id'] == int(data_id)][0]
        except IndexError:
            return []
    data_id = [i['id'] for i in data_id]
    answer_vote = [a for a in data if a['user_id']
                   == user_id and a['answer_id'] in data_id]
    while len(data_id) != len(answer_vote):
        answer_vote.append([])
    return answer_vote


def answer_sorting(answers, votes):
    """Takes in an answers and votes,
    sorts them and return it so it can be easily
    printed in html
    Args:
        answers (list): list of filtered answers
        votes (list): list of votes for those answers

    Returns:
        zip: zip (answer,votes)
    """
    for answer in answers:
        for vote in votes:
            if vote == []:
                continue
            if answer.get('id') == vote.get('answer_id'):
                x, y = answers.index(answer), votes.index(vote)
                votes[x], votes[y] = votes[y], votes[x]
    return zip(answers, votes)
