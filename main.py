from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

import os
import sqlite3

# 顧客追加フォームを読み込む
from forms import AddCustomerForm
from forms import AddTaskForm

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

#task_viewのページを作成します。
@app.route("/task_view")
def task_view_page():
    #DBからタスク一覧を取り出す
    filepath = "database/todo_app.db"
    con = sqlite3.connect(filepath)
    cur = con.cursor()
    # この中でクエリを書く
    #
    cur.execute("""
            SELECT
                * 
            FROM
                task
            LEFT JOIN
                customer
            ON
                task.customer_id = customer.customer_id 
            WHERE
                progress NOT IN ("完了")
            ORDER BY
                deadline
            """)
    tasks = cur.fetchall()
    con.close()

    return render_template("task_view.html" , tasks = tasks)

@app.route("/customer-<int:id>")
def customer_page(id):
    # DBから企業一覧を取り出す
    filepath = "database/todo_app.db"
    con = sqlite3.connect(filepath)
    cur = con.cursor()
    # この中でクエリを書く
    # 顧客情報
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

    # タスク情報
    cur.execute("""
            SELECT
                *
            FROM
                task
            """)
    tasks = cur.fetchall()
    con.close()

    return render_template("customer.html",id=id,items=items, tasks=tasks)

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
    form = AddTaskForm(request.form)
    # POST
    if request.method == "POST":
        # 顧客ID
        customer_id = form.customer_id.data
        # 先方の担当者様
        sir = form.sir.data
        # タスクの内容
        task_content = form.task_content.data
        #期日
        deadline = form.deadline.data
        #担当者
        pic = form.pic.data
        #タスクの進捗状況
        progress = form.progress.data
        
        # DBに顧客情報を追加する
        filepath = "database/todo_app.db"
        # databaseにレコードを追加
        con = sqlite3.connect(filepath)
        cur = con.cursor()
        cur.execute('INSERT INTO task (customer_id, sir, task_content, deadline, pic, progress) VALUES (?, ?, ?, ?, ?, ?)',
                    (customer_id, sir, task_content, deadline, pic, progress))
        con.commit()
        con.close()

        #出力
        return render_template("success_add_task.html", 
                               customer_id=customer_id, 
                               sir=sir,
                               task_content=task_content,
                               deadline=deadline,
                               pic=pic,
                               progress=progress)
    # GET
    else:
        return render_template("add_task.html", form=form)
# ▲▲▲---ココに、タスク追加をするページを作成してみよう！---▲▲▲

@app.route("/update_task-<int:task_id>", methods=["GET","POST"])
def update_task_page(task_id):
    form = AddTaskForm(request.form)
    # POST
    if request.method == "POST":
        # 顧客ID
        customer_id = form.customer_id.data
        # 先方の担当者様
        sir = form.sir.data
        # タスクの内容
        task_content = form.task_content.data
        #期日
        deadline = form.deadline.data
        #担当者
        pic = form.pic.data
        #タスクの進捗状況
        progress = form.progress.data
        
        # DBに顧客情報を追加する
        filepath = "database/todo_app.db"
        # databaseにレコードを追加
        con = sqlite3.connect(filepath)
        cur = con.cursor()
        cur.execute("""UPDATE
                            task
                        SET
                            customer_id=?,
                            sir=?,
                            task_content=?,
                            deadline=?,
                            pic=?,
                            progress=?
                        WHERE
                            task_id=?
                        """,
                    (customer_id, sir, task_content, deadline, pic, progress, task_id))
        con.commit()
        con.close()
        return redirect(url_for("task_view_page"))
    # GET
    else:
        return render_template("update_task.html", form=form, task_id=task_id)


if __name__ == "__main__":
    app.run(debug=True)