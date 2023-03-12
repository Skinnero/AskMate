from flask import Blueprint, request, redirect, url_for, render_template, session
from connection import ANSWER, QUESTION, COMMENT, QUESTION_TAG, TAG, USERS, USERS_VOTE
from util import prepare_question_before_saving, adding_valid_image_path, calculate_user_reputation, prepare_user_vote_before_saving,\
divide_vote_data, answer_sorting
from data_handler import read_all_data_from_db, insert_data_into_db, update_data_in_db, delete_data_in_db,\
read_single_row_from_db_by_id, take_tags_from_db_by_question_id, read_specified_lines_from_db,\
read_necessery_data_from_db_for_reputation_count


question_api = Blueprint('question_api', __name__)

@question_api.route("/question/<id>", methods=["GET"])
def question(id):
    vote_data = read_all_data_from_db(USERS_VOTE)
    question_votes = divide_vote_data('question',vote_data,session['user']['id'],id)
    question_data = read_single_row_from_db_by_id(QUESTION, id)
    answers_data = [a for a in read_all_data_from_db(ANSWER) if a['question_id'] == int(id)]
    answer_votes = divide_vote_data('answer',vote_data,session['user']['id'],answers_data)
    comment_data = read_all_data_from_db(COMMENT)
    answers_data = answer_sorting(answers_data,answer_votes)
    user_name = read_single_row_from_db_by_id(USERS, question_data['user_id'])
    tag_data = take_tags_from_db_by_question_id(id)
    question_data['view_number'] += 1
    update_data_in_db(QUESTION, question_data)
    return render_template("question.html",
                           question=question_data,
                           answers=answers_data,
                           comments=comment_data,
                           tags=tag_data,
                           user_name=user_name['user_name'],
                           question_votes=question_votes,)

@question_api.route("/add-question", methods=["GET", "POST"])
def question_add():
    if request.method == "GET":
        return render_template("add_question.html")
    else:
        data = request.form.to_dict()
        data['image'] = adding_valid_image_path(request.files['image'])
        data['user_id'] = session['user']['id']
        data = prepare_question_before_saving(data)
        insert_data_into_db(QUESTION, data)
        question = read_all_data_from_db(QUESTION)
        return redirect(url_for('question_api.question', id=question[0]['id']))


@question_api.route("/question/<id>/delete", methods=["GET"])
def question_delete(id):
    question = read_single_row_from_db_by_id(QUESTION, id)
    delete_data_in_db(QUESTION, question)
    return redirect(url_for("list_questions"))


@question_api.route("/question/<id>/edit", methods=['GET', 'POST'])
def question_edit(id):
    question = read_single_row_from_db_by_id(QUESTION, id)
    if request.method == 'GET':
        return render_template("edit_question.html", question=question)
    else:
        data = request.form.to_dict()
        image = adding_valid_image_path(request.files['image'])
        question['title'] = data['title']
        question['message'] = data['message']
        question['image'] = image if image != '' else question['image']
        update_data_in_db(QUESTION, question)
        return redirect(url_for("question_api.question", id=id))


@question_api.route("/question/<question_id>/vote-up", methods=["GET"])
def question_vote_up(question_id):
    if request.args.get('vote_exist'):
        vote = 1
        vote_data = prepare_user_vote_before_saving(session['user']['id'],vote,question_id=question_id)
        insert_data_into_db(USERS_VOTE,vote_data)
    else:
        vote_data = read_single_row_from_db_by_id(USERS_VOTE,request.args.get('question_votes'))
        vote = 2 if vote_data['voted'] == -1 else 1
        vote_data['voted'] = 1
        update_data_in_db(USERS_VOTE,vote_data)
    data = read_single_row_from_db_by_id(QUESTION, question_id)
    data['vote_number'] += vote
    update_data_in_db(QUESTION, data)
    update_data_in_db(USERS,calculate_user_reputation(read_necessery_data_from_db_for_reputation_count()))
    return redirect(url_for('question_api.question', id=question_id))


@question_api.route("/question/<question_id>/vote-down", methods=["GET"])
def question_vote_down(question_id):
    if request.args.get('vote_exist'):
        vote = -1
        vote_data = prepare_user_vote_before_saving(session['user']['id'],vote,question_id=question_id,)
        insert_data_into_db(USERS_VOTE,vote_data)
    else:
        vote_data = read_single_row_from_db_by_id(USERS_VOTE,request.args.get('question_votes'))
        vote = -2 if vote_data['voted'] == 1 else -1
        vote_data['voted'] = -1
        update_data_in_db(USERS_VOTE,vote_data)
    data = read_single_row_from_db_by_id(QUESTION, question_id)
    data['vote_number'] += vote
    update_data_in_db(QUESTION, data)
    update_data_in_db(USERS,calculate_user_reputation(read_necessery_data_from_db_for_reputation_count()))

    return redirect(url_for('question_api.question', id=question_id))

@question_api.route("/question/<question_id>/vote-neutral", methods=["GET"])
def question_vote_neutral(question_id):
    vote_data = read_single_row_from_db_by_id(USERS_VOTE,request.args.get('question_votes'))
    previous_vote = vote_data['voted']
    vote_data['voted'] = 0
    update_data_in_db(USERS_VOTE,vote_data)
    data = read_single_row_from_db_by_id(QUESTION, question_id)
    data['vote_number'] -= previous_vote
    update_data_in_db(QUESTION, data)
    update_data_in_db(USERS,calculate_user_reputation(read_necessery_data_from_db_for_reputation_count()))
    
    return redirect(url_for('question_api.question', id=question_id))

@question_api.route("/question/<question_id>/add-tag", methods=["GET", "POST"])
def question_add_tag(question_id):
    if request.method == 'GET':
        return render_template("add_tag.html", question_id=question_id)
    else:
        new_tag = request.form.to_dict()
        insert_data_into_db(TAG, new_tag)
        new_tag_id = read_specified_lines_from_db(TAG, "name = ", new_tag['name'], "id")[0]
        question_tag = {'question_id': question_id,'tag_id': new_tag_id['id']}
        insert_data_into_db(QUESTION_TAG, question_tag)
        return redirect(url_for("question_api.question", id=question_id))


@question_api.route("/question/<question_id>/tag/<tag_id>/delete", methods=["GET"])
def question_delete_tag(question_id, tag_id):
    tag = read_single_row_from_db_by_id(TAG, tag_id)
    delete_data_in_db(TAG, tag)
    return redirect(url_for("question_api.question", id=question_id))
