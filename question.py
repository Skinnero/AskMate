from flask import Blueprint, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from os import path
from connection import ANSWER, QUESTION, COMMENT, IMAGE_DATA
from util import prepare_question_before_saving
from data_handler import read_all_data_from_db, insert_data_into_db, update_data_in_db, delete_data_in_db, read_single_row_from_db

question_api = Blueprint('question_api', __name__)

@question_api.route("/question/<id>", methods=["GET"])
def route_question(id):
    question_data = read_single_row_from_db(QUESTION,id)
    answers_data = read_all_data_from_db(ANSWER)
    comment_data = read_all_data_from_db(COMMENT)
    question_data['view_number'] += 1
    update_data_in_db(QUESTION,question_data)
    return render_template("question.html", question=question_data, answers=answers_data, comments=comment_data)


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
        return redirect(url_for('question_api.route_question', id=question[-1]['id']))
    
@question_api.route("/question/<id>/delete", methods=["GET"])
def route_delete_question(id):
    question = read_single_row_from_db(QUESTION,id)
    delete_data_in_db(QUESTION, question)
    return redirect(url_for("route_list"))

@question_api.route("/question/<id>/edit", methods=['GET','POST'])
def route_edit_question(id):
    question = read_single_row_from_db(QUESTION,id)
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
    data = read_single_row_from_db(QUESTION,question_id)
    data['vote_number'] += 1
    update_data_in_db(QUESTION,data)
    return redirect(url_for("route_list"))

@question_api.route("/question/<question_id>/vote-down", methods=["GET"])
def route_question_vote_down(question_id):
    data = read_single_row_from_db(QUESTION,question_id)
    data['vote_number'] -= 1
    update_data_in_db(QUESTION,data)
    return redirect(url_for("route_list"))