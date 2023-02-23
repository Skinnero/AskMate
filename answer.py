from flask import Blueprint, request, render_template, url_for, redirect
from werkzeug.utils import secure_filename
from os import path
from util import prepare_answer_before_saving
from connection import ANSWER, QUESTION, IMAGE_DATA
from data_handler import insert_data_into_db, delete_data_in_db, update_data_in_db, read_single_row_from_db_by_id

answer_api = Blueprint('answer_api', __name__)

@answer_api.route("/question/<id>/add-answer", methods=["GET","POST"])
def route_answer_add(id):
    if request.method == 'GET':
        question = read_single_row_from_db_by_id(QUESTION,id)
        return render_template("add_answer.html", question=question)
    else:
        data = request.form.to_dict()
        file = request.files['image']
        if file.filename != '':
            filename = secure_filename(file.filename)
            file.save(path.join(IMAGE_DATA, filename))
        data['question_id'] = id
        data['image'] = file.filename
        data = prepare_answer_before_saving(data)
        insert_data_into_db(ANSWER, data)
        filename = secure_filename(file.filename)
        return redirect(url_for('question_api.route_question', id=id))

@answer_api.route("/answer/<answer_id>/edit", methods=['GET','POST'])
def route_answer_edit(answer_id):
    answer = read_single_row_from_db_by_id(ANSWER,answer_id)
    if request.method == 'GET':
        return render_template("edit_answer.html",answer=answer)
    else:
        file = request.files['image']
        if file.filename != '':
            filename = secure_filename(file.filename)
            file.save(path.join(IMAGE_DATA, filename))
        else:
            filename = answer['image']
        data = request.form.to_dict()
        answer['message'] = data['message']
        answer['image'] = filename
        update_data_in_db(ANSWER, answer)
        return redirect(url_for("question_api.route_question", id=answer['question_id']))


@answer_api.route("/answer/<answer_id>/delete", methods=['GET'])
def route_answer_delete(answer_id):
    data = read_single_row_from_db_by_id(ANSWER,answer_id)
    delete_data_in_db(ANSWER, data)
    return redirect(url_for('question_api.route_question', id=data['question_id']))

@answer_api.route("/answer/<answer_id>/vote_up", methods=["GET"])
def route_answer_vote_up(answer_id):
    data = read_single_row_from_db_by_id(ANSWER,answer_id)
    data['vote_number'] += 1
    update_data_in_db(ANSWER,data)
    return redirect(url_for("question_api.route_question", id = data['question_id']))

@answer_api.route("/answer/<answer_id>/vote_down", methods=["GET"])
def route_answer_vote_down(answer_id):
    data = read_single_row_from_db_by_id(ANSWER,answer_id)
    data['vote_number'] -= 1
    update_data_in_db(ANSWER,data)
    return redirect(url_for("question_api.route_question", id = data['question_id']))
    