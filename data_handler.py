from connection import CURSOR
from util import string_validity_checker
from psycopg2 import errors


def catch_all_key_from_db(table):
    """Takes in a table name and returns all column names
    in a list

    Args:
        table (str): name of a table

    Returns:
        list: list of column names
    """
    CURSOR.execute(f"SELECT * FROM {table} LIMIT 0")
    return [k[0] for k in CURSOR.description if k[0] != 'id']


def read_all_data_from_db(table):
    """Takes in a name of a table and returns all contents of it
    as a list of dict

    Args:
        table (str): name of a table

    Returns:
        list: list of dicts
    """
    CURSOR.execute(f"SELECT * FROM {table} ORDER BY id DESC")
    return CURSOR.fetchall()


def read_single_row_from_db_by_id(table, id):
    """Takes in a name of a table and returns single row
    with all of its data

    Args:
        table (str): name of a table

    Returns:
        dict: dicts with data
    """
    CURSOR.execute(f"SELECT * FROM {table} WHERE id='{id}'")
    return CURSOR.fetchone()


def insert_data_into_db(table, value):
    """Takes is name of a table and value.
    Inserts it to the table

    Args:
        table (str): name of a table
        value (dict): dict for a correct table
    """
    table_keys = catch_all_key_from_db(table)
    value = [v for v in value.values()]
    try:
        CURSOR.execute(
            f"INSERT INTO {table}({','.join(table_keys)}) VALUES("+"%s"+", %s"*(len(value)-1)+");", value)
        return True
    except errors.UniqueViolation:
        return False


def delete_data_in_db(table, value):
    """Takes in a name of a table and value.
    Deletes a row with id of a value

    Args:
        table (str): name of a table
        value (dict): dict for a correct table
    """
    CURSOR.execute(f"DELETE FROM {table} WHERE id = '{value['id']}';")


def update_data_in_db(table, value):
    """Takes in a name of a table and value.
    Updates every columns by values id.

    Args:
        table (str): name of a table
        value (dict): dict for a correct table
    """
    if type(value) != list:
        for k, v in value.items():
            if v == None:
                continue
            if type(v) == str:
                v = string_validity_checker(v)
            CURSOR.execute(f"UPDATE {table} SET {k} = '{v}' WHERE id = {value['id']}")
    else:
        for data in value:
            update_data_in_db(table, data)


def take_tags_from_db_by_question_id(id):
    """Searches the db's and looks for name of a tag with a question_id

    Args:
        id (int): question_id number

    Returns:
        list: list of dicts
    """
    CURSOR.execute(f"SELECT tag_id FROM question_tag WHERE question_id = {id}")
    data = CURSOR.fetchall()
    if data == []:
        return []
    tag_id = [str(k.get('tag_id')) for k in data]
    CURSOR.execute(
        f"SELECT * FROM tag WHERE id IN ({', '.join(tag_id)}) ORDER BY name")
    return CURSOR.fetchall()


def read_specified_lines_from_db(table, where, condition, column='*'):
    """Takes in table, where_condition, column
    to write select querry in db e.g.
    SELECT columnt FROM table WHERE where_condition.
    everytinh must be correct in string

    Args:
        table (str): name of a table
        where_condition (str): str of after where condition
        column (str, optional): str of a column. Defaults to '*'.

    Returns:
        list: list of dicts
    """
    CURSOR.execute(
        f"SELECT {column} FROM {table} WHERE {where}{'%s'}", (condition,))
    return CURSOR.fetchall()


def sort_db_by_order(table, order_by, order_direction):
    """Sorts the table depending on a button urser proviedes

    Args:
        table (str): name of a table
        order_by (str): name of a column
        order_direction (str): direction

    Returns:
        list: list of sorted dicts
    """
    # TODO: Secure query
    CURSOR.execute(
        f"SELECT * FROM {table} ORDER BY {order_by} {order_direction};")
    return CURSOR.fetchall()


def search_db_by_string(text, order_by=None, order_direction=None):
    """Looks through db in search for a text
    and returns on inner join question.id = answer.question_id.
    It seraches only by question.title, question.message, answer.message

    Args:
        text (str): search string

    Returns:
        list: list of dicts
    """
    # Handling empty orders
    # TODO: Sacure query
    if order_by == None:
        order_by, order_direction = ('id', 'asc')
    text = text.lower()
    CURSOR.execute(f""" SELECT DISTINCT question.id, question.title, question.submission_time, question.message,
                        question.view_number, question.vote_number
                        FROM question LEFT JOIN answer ON question.id=answer.question_id WHERE LOWER(question.title) LIKE '%{text}%'
                        OR LOWER(question.message) LIKE '%{text}%' OR LOWER(answer.message) LIKE '%{text}%'
                        ORDER BY {order_by} {order_direction};""")
    return CURSOR.fetchall()


def five_latest_question_from_db():
    """Return 5 latest question

    Returns:
        list: list of dicts
    """
    CURSOR.execute(
        f"SELECT question.title, question.message FROM question ORDER BY submission_time desc LIMIT 5")
    return CURSOR.fetchall()


def count_question_answer_comment_from_db_by_user(where=''):
    """Return count of question, answer and comment by user.
    You can provide where parametr if specified needed.

    Args:
        where (str, optional): You have to provide whole queri starting with
        "WHERE to end". Defaults to ''.

    Returns:
        list: list of dicts
    """
    CURSOR.execute(f"""
                        SELECT DISTINCT users.id user_name, COUNT(DISTINCT question.id) AS question_count,
                        COUNT(DISTINCT answer.id) AS answer_count, COUNT(DISTINCT comment.id) AS comment_count 
                        FROM users LEFT JOIN question ON users.id=question.user_id 
                        LEFT JOIN answer ON users.id=answer.user_id 
                        LEFT JOIN comment ON users.id=comment.user_id
                        {where}
                        GROUP BY user_name, users.id ORDER BY users.id 
                        """)
    return CURSOR.fetchall()


def read_necessery_data_from_db_for_reputation_count():

    CURSOR.execute("""
                        SELECT users.id, SUM(DISTINCT CASE WHEN question.vote_number > 0 THEN question.vote_number ELSE 0 END) AS question_vote_up,
                        SUM(DISTINCT CASE WHEN question.vote_number < 0 THEN question.vote_number ELSE 0 END) AS question_vote_down,
                        SUM(DISTINCT CASE WHEN answer.vote_number > 0 THEN answer.vote_number ELSE 0 END) AS answer_vote_up,
                        SUM(CASE WHEN answer.vote_number < 0 THEN answer.vote_number ELSE 0 END) AS answer_vote_down,
                        COUNT(DISTINCT CASE WHEN answer.accepted = 2 THEN answer.accepted ELSE 0 END) AS answer_accepted
                        FROM users LEFT JOIN question ON users.id=question.user_id LEFT JOIN answer ON users.id=answer.user_id GROUP BY users.id;
                        """)

    return CURSOR.fetchall()
