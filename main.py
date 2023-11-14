from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.route("/")
def top_page():
    return render_template("top.html")


@app.route("/customer_list")
def customer_list_page():
    return render_template("customer_list.html")


@app.route("/task")
def task_page():
    return render_template("task.html")



"""
if __name__ == "__main__":
    app.run()
"""