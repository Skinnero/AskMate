from flask import Flask, render_template, send_from_directory, request
from route.question import question_api
from route.answer import answer_api
from route.comment import comment_api
from route.user import user_api
from connection import QUESTION, IMAGE_DATA, TAG
from data_handler import read_all_data_from_db, sort_db_by_order, search_db_by_string, five_latest_question_from_db

app = Flask(__name__, template_folder='templates', static_folder='static', )
app.secret_key = b'secret_code'
app.register_blueprint(question_api)
app.register_blueprint(answer_api)
app.register_blueprint(comment_api)
app.register_blueprint(user_api)


@app.route('/images/<filename>')
def image(filename):
    return send_from_directory(IMAGE_DATA, filename)


@app.route("/about_us")
def about_us():
    return render_template("about_us.html")


@app.route("/")
def home():
    questions = five_latest_question_from_db()
    return render_template("index.html", questions=questions)


@app.route("/list", methods=["GET"])
def list_questions():
    questions = read_all_data_from_db(QUESTION)
    if request.args.get("order_by") != None and request.args.get("order_direction") != None:
        order_by = request.args.get("order_by")
        order_direction = request.args.get("order_direction")
        questions = sort_db_by_order(QUESTION, order_by, order_direction)
    return render_template("list.html", questions=questions)


@app.route("/search", methods=["GET"])
def search():
    search = request.args.get('search')
    questions = search_db_by_string(search, request.args.get(
        "order_by"), request.args.get("order_direction"))
    return render_template("search.html", questions=questions, search=search)

@app.route('/tags')
def tags():
    tags = read_all_data_from_db(TAG)
    return render_template("tags.html", tags=tags)

if __name__ == "__main__":
    app.run(

        host="0.0.0.0",
        debug=True,
    )
