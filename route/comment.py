from flask import Blueprint, request, redirect, url_for, render_template, session
from util import prepare_comment_before_saving
from data_handler import insert_data_into_db, read_single_row_from_db_by_id, delete_data_in_db, update_data_in_db
from connection import COMMENT, ANSWER, QUESTION


comment_api = Blueprint('comment_api', __name__)


@comment_api.route('/question/<question_id>/add-comment', methods=["GET", "POST"])
def comment_add_to_question(question_id):
    if request.method == "GET":
        question = read_single_row_from_db_by_id(QUESTION, question_id)
        return render_template("/add_comment_to_question.html", question=question)
    else:
        data = request.form.to_dict()
        data['question_id'] = question_id
        data['user_id'] = session['user']['id']
        comment_data = prepare_comment_before_saving(data)
        insert_data_into_db(COMMENT, comment_data)
        return redirect(url_for('question_api.question', id=question_id))


@comment_api.route('/answer/<answer_id>/add-comment', methods=["GET", "POST"])
def comment_add_to_answer(answer_id):
    answer = read_single_row_from_db_by_id(ANSWER, answer_id)
    if request.method == "GET":
        return render_template("/add_comment_to_answer.html", answer=answer)
    else:
        data = request.form.to_dict()
        data['answer_id'] = answer_id
        data['user_id'] = session['user']['id']
        data['question_id'] = answer['question_id']
        comment_data = prepare_comment_before_saving(data)
        insert_data_into_db(COMMENT, comment_data)
        return redirect(url_for('question_api.question', id=answer['question_id']))


@comment_api.route("/comment/<comment_id>/edit", methods=['GET', 'POST'])
def comment_edit(comment_id):
    comment = read_single_row_from_db_by_id(COMMENT, comment_id)
    if request.method == 'GET':
        return render_template("edit_comment.html", comment=comment)
    else:
        data = request.form.to_dict()
        comment['message'] = data['message']
        comment['edited_count'] += 1
        question = read_single_row_from_db_by_id(QUESTION, comment['question_id'])
        update_data_in_db(COMMENT, comment)
        return redirect(url_for("question_api.question", id=question['id']))


@comment_api.route("/comments/<comment_id>/delete", methods=["GET"])
def comment_delete(comment_id):
    comment = read_single_row_from_db_by_id(COMMENT, comment_id)
    id = read_single_row_from_db_by_id(ANSWER, comment['answer_id'])[
        'question_id'] if comment.get('question_id') == None else comment['question_id']
    delete_data_in_db(COMMENT, comment)
    return redirect(url_for('question_api.question', id=id))
