from flask import Blueprint, request, redirect, url_for, render_template, jsonify
from werkzeug.utils import secure_filename
from os import path
from connection import ANSWER, QUESTION, COMMENT, IMAGE_DATA, QUESTION_TAG, TAG
from util import prepare_question_before_saving
from data_handler import read_all_data_from_db, insert_data_into_db, update_data_in_db, delete_data_in_db, read_single_row_from_db_by_id, take_tags_from_db_by_question_id, read_from_db

question_api = Blueprint('question_api', __name__)

@question_api.route("/question/<id>", methods=["GET"])
def route_question(id):
    question_data = read_single_row_from_db_by_id(QUESTION,id)
    answers_data = read_all_data_from_db(ANSWER)
    comment_data = read_all_data_from_db(COMMENT)
    tag_data = take_tags_from_db_by_question_id(id)
    question_data['view_number'] += 1
    update_data_in_db(QUESTION,question_data)
    return render_template("question.html", question=question_data, answers=answers_data, comments=comment_data, tags=tag_data)


@question_api.route("/add-question", methods=["GET","POST"])
def route_question_add():
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
def route_question_delete(id):
    question = read_single_row_from_db_by_id(QUESTION,id)
    delete_data_in_db(QUESTION, question)
    return redirect(url_for("route_list"))

@question_api.route("/question/<id>/edit", methods=['GET','POST'])
def route_question_edit(id):
    question = read_single_row_from_db_by_id(QUESTION,id)
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
    data = read_single_row_from_db_by_id(QUESTION,question_id)
    data['vote_number'] += 1
    update_data_in_db(QUESTION,data)
    return redirect(url_for('question_api.route_question', id=question_id))

@question_api.route("/question/<question_id>/vote-down", methods=["GET"])
def route_question_vote_down(question_id):
    data = read_single_row_from_db_by_id(QUESTION,question_id)
    data['vote_number'] -= 1
    update_data_in_db(QUESTION,data)
    return redirect(url_for('question_api.route_question', id=question_id))

@question_api.route("/question/<question_id>/add-tag", methods=["GET","POST"])
def route_question_add_tag(question_id):
    if request.method == 'GET':
        return render_template("add_tag.html",question_id=question_id)
    else:
        new_tag = request.form.to_dict()
        insert_data_into_db(TAG, new_tag)
        new_tag_id = read_from_db(TAG,f"name=\'{new_tag['name']}\'","id")
        question_tag = {'question_id':question_id,'tag_id':new_tag_id[0]['id']}
        insert_data_into_db(QUESTION_TAG,question_tag)
        return redirect(url_for("question_api.route_question", id=question_id))
    
@question_api.route("/question/<question_id>/tag/<tag_id>/delete", methods=["GET"])
def route_question_delete_tag(question_id,tag_id):
    tag = read_single_row_from_db_by_id(TAG,tag_id)
    delete_data_in_db(TAG, tag)
    return redirect(url_for("question_api.route_question", id=question_id))