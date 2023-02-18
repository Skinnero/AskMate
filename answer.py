from flask import Blueprint, request, render_template, url_for, redirect
from werkzeug.utils import secure_filename
from os import path
from util import get_data_by_id, vote_changer
from connection import QUESTION_DATA, ANSWER_DATA, IMAGE_DATA
from data_handler import adding_to_file, delete_data_from_file

answer_api = Blueprint('answer_api', __name__)

@answer_api.route("/question/<id>/add-answer", methods=["GET","POST"])
def route_add_answer(id):
    if request.method == 'GET':
        question = get_data_by_id(id, QUESTION_DATA)
        return render_template("add_answer.html", question=question)
    else:
        data = request.form.to_dict()
        file = request.files['image']
        if file.filename != '':
            filename = secure_filename(file.filename)
            file.save(path.join(IMAGE_DATA, filename))
        data['question_id'] = id
        data['image'] = file.filename
        adding_to_file(ANSWER_DATA, data)
        filename = secure_filename(file.filename)
        return redirect(url_for('question_api.route_question', id=id))

@answer_api.route("/answer/<answer_id>/delete", methods=['GET'])
def route_delete_answer(answer_id):
    answer = get_data_by_id(answer_id,ANSWER_DATA)
    delete_data_from_file(ANSWER_DATA, answer)
    return redirect(url_for('question_api.route_question', id=answer['question_id']))

@answer_api.route("/answer/<answer_id>/vote_up", methods=["GET"])
def route_answer_vote_up(answer_id):
    answer = get_data_by_id(answer_id, ANSWER_DATA)
    vote_changer(ANSWER_DATA, answer, True)
    return redirect(url_for("question_api.route_question", id = answer['question_id']))

@answer_api.route("/answer/<answer_id>/vote_down", methods=["GET"])
def route_answer_vote_down(answer_id):
    answer = get_data_by_id(answer_id, ANSWER_DATA)
    vote_changer(ANSWER_DATA, answer, False)
    return redirect(url_for("question_api.route_question", id = answer['question_id']))
    