from flask import Blueprint, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from os import path
from connection import ANSWER, QUESTION, IMAGE_DATA
from util import get_data_by_id, prepare_question_before_saving
from data_handler import read_all_data_from_db, insert_data_into_db, update_data_in_db, delete_data_in_db

question_api = Blueprint('question_api', __name__)

@question_api.route("/question/<id>", methods=["GET"])
def route_question(id):
    question_data = get_data_by_id(id, read_all_data_from_db(QUESTION))
    answers_data = read_all_data_from_db(ANSWER)
    question_data['view_number'] += 1
    update_data_in_db(QUESTION,question_data)
    return render_template("question.html", question=question_data, answers=answers_data,)


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
        data = prepare_question_before_saving(data)
        insert_data_into_db(QUESTION, data)
        question = read_all_data_from_db(QUESTION)
        print(question)
        return redirect(url_for('question_api.route_question', id=question[-1]['id']))
    
@question_api.route("/question/<id>/delete", methods=["GET"])
def route_delete_question(id):
    question = get_data_by_id(id,read_all_data_from_db(QUESTION))
    delete_data_in_db(QUESTION, question)
    return redirect(url_for("route_list"))

@question_api.route("/question/<id>/edit", methods=['GET','POST'])
def route_edit_question(id):
    question = get_data_by_id(id,read_all_data_from_db(QUESTION))
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
        question['title'] = data['title']
        question['message'] = data['message']
        question['image'] = filename
        update_data_in_db(QUESTION, question)
        return redirect(url_for("question_api.route_question", id=id))
      
@question_api.route("/question/<question_id>/vote-up", methods=["GET"])
def route_question_vote_up(question_id):
    data = get_data_by_id(question_id, read_all_data_from_db(QUESTION))
    data['vote_number'] += 1
    update_data_in_db(QUESTION,data)
    return redirect(url_for("route_list"))

@question_api.route("/question/<question_id>/vote-down", methods=["GET"])
def route_question_vote_down(question_id):
    data = get_data_by_id(question_id, read_all_data_from_db(QUESTION))
    data['vote_number'] -= 1
    update_data_in_db(QUESTION,data)
    return redirect(url_for("route_list"))