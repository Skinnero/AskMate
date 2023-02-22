from flask import Blueprint, request, redirect, url_for, render_template
from util import prepare_comment_before_saving
from data_handler import insert_data_into_db, read_single_row_from_db, delete_data_in_db, update_data_in_db
from connection import COMMENT, ANSWER


comment_api = Blueprint('comment_api', __name__)

@comment_api.route('/question/<question_id>/add-comment',methods=["GET","POST"])
def route_add_comment_to_question(question_id):
    if request.method == "GET":
        return render_template("/add_comment_to_question.html", question_id=question_id)
    else:
        data = request.form.to_dict()
        data['question_id'] = question_id
        comment_data = prepare_comment_before_saving(data)
        insert_data_into_db(COMMENT,comment_data)
        return redirect(url_for('question_api.route_question', id=question_id))
    
@comment_api.route('/answer/<answer_id>/add-comment',methods=["GET","POST"])
def route_add_comment_to_answer(answer_id):
    if request.method == "GET":
        return render_template("/add_comment_to_answer.html", answer_id=answer_id)
    else:
        data = request.form.to_dict()
        data['answer_id'] = answer_id
        comment_data = prepare_comment_before_saving(data)
        answer_data = read_single_row_from_db(ANSWER,answer_id)
        print(comment_data)
        insert_data_into_db(COMMENT,comment_data)
        return redirect(url_for('question_api.route_question', id=answer_data['question_id']))

@comment_api.route("/comment/<comment_id>/edit", methods=['GET','POST'])
def route_edit_comment(comment_id):
    comment = read_single_row_from_db(COMMENT,comment_id)
    if request.method == 'GET':
        return render_template("edit_comment.html",comment=comment)
    else:
        data = request.form.to_dict()
        comment['message'] = data['message']
        comment['edited_count'] += 1
        answer = read_single_row_from_db(ANSWER,comment['answer_id'])
        update_data_in_db(COMMENT, comment)
        return redirect(url_for("question_api.route_question", id=answer['question_id']))


@comment_api.route("/comments/<comment_id>/delete", methods=["GET"])
def route_delete_comment(comment_id):
    comment = read_single_row_from_db(COMMENT,comment_id)
    id = read_single_row_from_db(ANSWER,comment['answer_id'])['question_id'] if comment.get('question_id') == None else comment['question_id']
    delete_data_in_db(COMMENT, comment)
    return redirect(url_for('question_api.route_question', id=id))