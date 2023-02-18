from flask import Blueprint, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from os import path
from connection import QUESTION_DATA, ANSWER_DATA, IMAGE_DATA, read_csv_file
from util import get_data_by_id, vote_changer, question_view_number_changer
from data_handler import delete_answers_to_question, delete_data_from_file, adding_to_file, edit_data

question_api = Blueprint('question_api', __name__)

@question_api.route("/question/<id>", methods=["GET"])
def route_question(id):
    question = get_data_by_id(id, QUESTION_DATA)
    answers = read_csv_file(ANSWER_DATA)
    question_view_number_changer(QUESTION_DATA, question)
    return render_template("question.html", question=question, answers=answers,)


@question_api.route("/add-question", methods=["GET","POST"])
def route_add_question():
    if request.method == "GET":
        return render_template("add_question.html")
    else:
        file = request.files['image']
        if file.filename != '':
            filename = secure_filename(file.filename)
            file.save(path.join(IMAGE_DATA, filename))
        data = request.form.to_dict()
        data['image'] = file.filename
        adding_to_file(QUESTION_DATA, data)
        file_data = read_csv_file(QUESTION_DATA)
        return redirect(url_for('question_api.route_question', id=(len(file_data))))
    
@question_api.route("/question/<id>/delete", methods=["GET"])
def route_delete_question(id):
    question = get_data_by_id(id,QUESTION_DATA)
    delete_data_from_file(QUESTION_DATA, question)
    delete_answers_to_question(ANSWER_DATA,id)
    return redirect(url_for("route_list"))

@question_api.route("/question/<id>/edit", methods=['GET','POST'])
def route_edit_question(id):
    question = get_data_by_id(id,QUESTION_DATA)
    if request.method == 'GET':
        return render_template("edit_question.html",question=question)
    else:
        file = request.files['image']
        if file.filename != '':
            filename = secure_filename(file.filename)
            file.save(path.join(IMAGE_DATA, filename))
        else:
            filename = question['image']
        data = request.form.to_dict()
        data['image'] = filename
        edit_data(QUESTION_DATA, data, question)
        return redirect(url_for("question_api.route_question", id=id))
      
@question_api.route("/question/<question_id>/vote-up", methods=["GET"])
def route_question_vote_up(question_id):
    question = get_data_by_id(question_id, QUESTION_DATA)
    vote_changer(QUESTION_DATA, question, True)
    return redirect(url_for("route_list"))

@question_api.route("/question/<question_id>/vote-down", methods=["GET"])
def route_question_vote_down(question_id):
    question = get_data_by_id(question_id, QUESTION_DATA)
    vote_changer(QUESTION_DATA, question, False)
    return redirect(url_for("route_list"))