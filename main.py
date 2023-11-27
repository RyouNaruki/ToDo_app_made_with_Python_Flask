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
    # この中でクエリを書く
    cur.execute("""
            SELECT
                customer_id,
                company,
                tel,
                email,
                contract_name
            FROM
                customer
            LEFT JOIN
                contract
            ON
                customer.is_contract = contract.contract_id
            """)
    items = cur.fetchall()
    con.close()
    return render_template("customer_list.html", items = items)

@app.route("/task_view")
def task_view_page():
    return render_template("task_view.html")

@app.route("/customer-<int:id>")
def customer_page(id):
    # DBから企業一覧を取り出す
    filepath = "database/todo_app.db"
    con = sqlite3.connect(filepath)
    cur = con.cursor()
    # この中でクエリを書く
    cur.execute("""
            SELECT
                customer_id,
                company,
                tel,
                email,
                contract_name
            FROM
                customer
            LEFT JOIN
                contract
            ON
                customer.is_contract = contract.contract_id
            """)
    items = cur.fetchall()
    con.close()

    return render_template("customer.html",id=id,items=items)

@app.route("/add_customer", methods=["GET","POST"])
def add_customer_page():
    form = AddCustomerForm(request.form)
    # POST
    if request.method == "POST":
        # 会社名
        company = form.company.data
        # お電話番号
        tel = form.tel.data
        # メールアドレス
        email = form.email.data

        # 契約状況（新たな顧客追加なので強制的に1となる）
        is_contract = 1

        # DBに顧客情報を追加する
        filepath = "database/todo_app.db"
        # databaseにレコードを追加
        con = sqlite3.connect(filepath)
        cur = con.cursor()
        cur.execute('INSERT INTO customer (company, tel, email, is_contract) VALUES (?, ?, ?, ?)',
                    (company, tel, email, is_contract))
        con.commit()
        con.close()

        # データ出力
        return render_template("success_add_customer.html",company=company,tel=tel,email=email)
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