from flask import Flask
from flask import render_template
from flask import request
import os
import sqlite3

# 顧客追加フォームを読み込む
from forms import AddCustomerForm

app = Flask(__name__)

@app.route("/")
def top_page():
    return render_template("top.html")

@app.route("/customer_list")
def customer_list_page():
    # DBから企業一覧を取り出す
    filepath = "database/todo_app.db"
    con = sqlite3.connect(filepath)
    cur = con.cursor()
    cur.execute("SELECT * FROM customer") # この中でクエリを書く
    items = cur.fetchall()
    con.close()
    return render_template("customer_list.html", items = items)

@app.route("/task")
def task_page():
    return render_template("task.html")

@app.route("/customer-<int:id>")
def customer_page(id):
    # DBから企業一覧を取り出す
    filepath = "database/todo_app.db"
    con = sqlite3.connect(filepath)
    cur = con.cursor()
    cur.execute("SELECT * FROM customer") # この中でクエリを書く
    items = cur.fetchall()
    con.close()

    return render_template("customer.html",id=id,items=items)

@app.route("/add_customer", methods=["GET","POST"])
def add_customer_page():
    form = AddCustomerForm(request.form)
    # POST
    if request.method == "POST":
        # お名前
        name = form.name.data
        # 会社名
        company = form.company.data
        # お電話番号
        tel = form.tel.data
        # メールアドレス
        email = form.email.data

        # DBに顧客情報を追加する
        filepath = "database/todo_app.db"
        # databaseにレコードを追加
        con = sqlite3.connect(filepath)
        cur = con.cursor()
        cur.execute('INSERT INTO customer (name, company, tel, email) VALUES (?, ?, ?, ?)',
                    (name, company, tel, email))
        con.commit()
        con.close()

        # データ出力
        return render_template("success.html",name=name,company=company,tel=tel,email=email)
    # GET
    else:
        return render_template("add_customer.html", form=form)

# ▼▼▼---ココに、タスク追加をするページを作成してみよう！---▼▼▼
@app.route("/add_task", methods=["GET","POST"])
def add_task_page():
    return render_template("add_task.html")
# ▲▲▲---ココに、タスク追加をするページを作成してみよう！---▲▲▲



if __name__ == "__main__":
    app.run(debug=True)