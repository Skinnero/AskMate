from flask import Flask, render_template, request, send_from_directory
from question import question_api
from answer import answer_api
from connection import QUESTION_DATA, IMAGE_DATA, ANSWER_DATA, read_csv_file
from data_handler import sort_table, manage_id_data

app = Flask(__name__, template_folder='templates', static_folder='static', )
app.register_blueprint(question_api)
app.register_blueprint(answer_api)

@app.route('/images/<filename>')
def route_image(filename):
    return send_from_directory(IMAGE_DATA, filename)

@app.route("/")
def route_home():
    return render_template("index.html")

@app.route("/list", methods=["GET"])
def route_list():
    questions = read_csv_file(QUESTION_DATA)
    manage_id_data(QUESTION_DATA)
    manage_id_data(ANSWER_DATA)
    # Sort list page
    if request.args.get("order_by") != None and request.args.get("order_direction") != None:
        order_by = request.args.get("order_by")
        order_direction = request.args.get("order_direction")
        questions = sort_table(order_by,order_direction,questions)
        return render_template("list.html", questions=questions)
    return render_template("list.html", questions=questions)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=7000,
        debug=True,
    )