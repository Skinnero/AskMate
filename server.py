from flask import Flask, render_template, send_from_directory, request, redirect, url_for
from question import question_api
from answer import answer_api
from comment import comment_api
from connection import QUESTION, IMAGE_DATA
from data_handler import read_all_data_from_db, sort_questions_by_order, search_database_by_string

app = Flask(__name__, template_folder='templates', static_folder='static', )
app.register_blueprint(question_api)
app.register_blueprint(answer_api)
app.register_blueprint(comment_api)

@app.route('/images/<filename>')
def route_image(filename):
    return send_from_directory(IMAGE_DATA, filename)

@app.route("/")
def route_home():
    return render_template("index.html")

@app.route("/list", methods=["GET"])
def route_list():
    questions = read_all_data_from_db(QUESTION)
    # Sort list page
    if request.args.get("search") != None:
        return redirect(url_for("route_search",search=request.args.get("search")))
    if request.args.get("order_by") != None and request.args.get("order_direction") != None:
        order_by = request.args.get("order_by")
        order_direction = request.args.get("order_direction")
        questions = sort_questions_by_order(QUESTION,order_by,order_direction)
    return render_template("list.html", questions=questions)

@app.route("/search", methods=["GET"])
def route_search():
    questions = search_database_by_string(request.args.get('search'))
    print(questions)
    return render_template("search.html", questions=questions)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=7000,
        debug=True,
    )