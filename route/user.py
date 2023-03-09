from flask import Blueprint, render_template, request, redirect, url_for, session
from util import create_password, prepare_user_before_saving, verify_password
from data_handler import insert_data_into_db, read_specified_lines_from_db, read_all_data_from_db,\
    count_question_answer_comment_from_db_by_user
from connection import USERS, QUESTION, ANSWER, COMMENT, USERS_VOTE


user_api = Blueprint('user_api', __name__)


@user_api.route('/registration', methods=['POST', 'GET'])
def registration():

    if request.method == "POST":
        data = request.form.to_dict()
        data['user_password'] = create_password(data['user_password'])
        data = prepare_user_before_saving(data)
        if not insert_data_into_db(USERS, data):
            message = 'That email or user name are already in use!'
            return render_template('registration.html', message=message)
        return redirect(url_for('home'))

    return render_template('registration.html')


@user_api.route('/login', methods=["POST", "GET"])
def login():

    if request.method == "POST":
        message = 'Email or password are incorrect'
        try:
            user_data = read_specified_lines_from_db(USERS,
                                                     "email = ",
                                                     request.form['user_email'])[0]
        except IndexError:
            return render_template('login.html', message=message)
        if verify_password(request.form['user_password'].encode(), user_data['password'].encode()):
            session['user'] = user_data
            session['user_vote'] = read_specified_lines_from_db(USERS_VOTE,'user_id = ',session['user']['id'])
            session.permanent = False
            return redirect(url_for('home'))
        else:
            return render_template('login.html', message=message)

    return render_template('login.html')


@user_api.route('/user')
def user():

    users = read_all_data_from_db(USERS)
    users_count = count_question_answer_comment_from_db_by_user()
    users = (zip(users, users_count))
    return render_template('user.html', users=users, users_count=users_count)


@user_api.route('/user/<user_id>')
def user_profile(user_id):

    questions = read_specified_lines_from_db(QUESTION, 'user_id = ', user_id)
    answers = read_specified_lines_from_db(ANSWER, 'user_id = ', user_id)
    comments = read_specified_lines_from_db(COMMENT, 'user_id = ', user_id)
    users_count = count_question_answer_comment_from_db_by_user(f"WHERE users.id = '{user_id}'")[0]
    return render_template('user_profile.html', questions=questions, answers=answers, comments=comments, users_count=users_count)


@user_api.route('/logout')
def logout():

    session.pop('user')
    return render_template('index.html')
