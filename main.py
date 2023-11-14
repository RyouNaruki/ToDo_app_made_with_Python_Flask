from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)


from forms import UserInfoForm


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

@app.route("/add_customer", methods=["GET","POST"])
def add_customer_page():
    form = UserInfoForm(request.form)

    # POST
    if request.method == "POST":
        return render_template("success.html")
    # GET
    else:
        return render_template("add_customer.html", form=form)

"""
if __name__ == "__main__":
    app.run(debug=True)
"""