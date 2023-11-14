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

@app.route("/customer")
def customer_page():
    return render_template("customer.html")

@app.route("/add_customer")
def add_customer_page():
    return render_template("add_customer.html")

if __name__ == "__main__":
    app.run(debug=True)
