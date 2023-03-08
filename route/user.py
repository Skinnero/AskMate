from flask import Blueprint, render_template, request, redirect, url_for
from util import create_password, prepare_user_before_saving
from data_handler import insert_data_into_db
from connection import USERS


user_api = Blueprint('user_api', __name__)
user_api.secret_key = b'secret_code'

@user_api.route('/registration', methods=['POST','GET'])
def registration():

    if request.method == "POST":
        data = request.form.to_dict()
        data['user_password'] = create_password(data['user_password'])
        data = prepare_user_before_saving(data)
        insert_data_into_db(USERS,data)
        return redirect(url_for('home'))

    return render_template('registration.html')