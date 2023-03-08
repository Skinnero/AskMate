from flask import Blueprint, request, render_template, url_for, redirect, session
from util import prepare_answer_before_saving, adding_valid_image_path
from connection import ANSWER, QUESTION
from data_handler import insert_data_into_db, delete_data_in_db, update_data_in_db, read_single_row_from_db_by_id

answer_api = Blueprint('answer_api', __name__)


@answer_api.route("/question/<id>/add-answer", methods=["GET", "POST"])
def answer_add(id):
    if request.method == 'GET':
        question = read_single_row_from_db_by_id(QUESTION, id)
        return render_template("add_answer.html", question=question)
    else:
        data = request.form.to_dict()
        data['question_id'] = id
        data['user_id'] = session['user']['id']
        data['image'] = adding_valid_image_path(request.files['image'])
        data = prepare_answer_before_saving(data)
        insert_data_into_db(ANSWER, data)
        return redirect(url_for('question_api.question', id=id))


@answer_api.route("/answer/<answer_id>/edit", methods=['GET', 'POST'])
def answer_edit(answer_id):
    answer = read_single_row_from_db_by_id(ANSWER, answer_id)
    if request.method == 'GET':
        return render_template("edit_answer.html", answer=answer)
    else:
        data = request.form.to_dict()
        image = adding_valid_image_path(request.files['image'])
        answer['message'] = data['message']
        answer['image'] = image if image != '' else answer['image']
        update_data_in_db(ANSWER, answer)
        return redirect(url_for("question_api.question", id=answer['question_id']))


@answer_api.route("/answer/<answer_id>/delete", methods=['GET'])
def answer_delete(answer_id):
    data = read_single_row_from_db_by_id(ANSWER, answer_id)
    delete_data_in_db(ANSWER, data)
    return redirect(url_for('question_api.question', id=data['question_id']))


@answer_api.route("/answer/<answer_id>/vote_up", methods=["GET"])
def answer_vote_up(answer_id):
    data = read_single_row_from_db_by_id(ANSWER, answer_id)
    data['vote_number'] += 1
    update_data_in_db(ANSWER, data)
    return redirect(url_for("question_api.question", id=data['question_id']))


@answer_api.route("/answer/<answer_id>/vote_down", methods=["GET"])
def answer_vote_down(answer_id):
    data = read_single_row_from_db_by_id(ANSWER, answer_id)
    data['vote_number'] -= 1
    update_data_in_db(ANSWER, data)
    return redirect(url_for("question_api.question", id=data['question_id']))
