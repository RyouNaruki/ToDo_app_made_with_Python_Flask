from flask import Flask, flash
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

import os
import sqlite3

# 顧客登録フォームを読み込む
from forms import AddCustomerForm
from forms import AddTaskForm

app = Flask(__name__)
app.secret_key = 'user'

@app.route("/")
def top_page():
    return render_template("top.html")

@app.route("/customer_list")
def customer_list_page():
    # DBから企業一覧を取り出す
    filepath = "database/app.db"
    con = sqlite3.connect(filepath)
    cur = con.cursor()
    # この中でクエリを書く
    cur.execute("""
            SELECT
                customer_id,
                company,
                address,
                tel,
                email,
                contract
            FROM
                customer
            WHERE
                contract NOT IN ('解約済み')
            """)
    items = cur.fetchall()
    con.close()
    return render_template("customer_list.html", items = items)

#task_viewのページを作成します。
@app.route("/task_view")
def task_view_page():
    #DBからタスク一覧を取り出す
    filepath = "database/app.db"
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
                AND deleted_at IS NULL
            ORDER BY
                deadline
            """)
    tasks = cur.fetchall()
    con.close()

    return render_template("task_view.html" , tasks = tasks)

@app.route("/customer-<int:id>")
def customer_page(id):
    # DBから企業一覧を取り出す
    filepath = "database/app.db"
    con = sqlite3.connect(filepath)
    cur = con.cursor()
    # この中でクエリを書く
    # 顧客情報
    cur.execute("""
            SELECT
                customer_id,
                company,
                address,
                tel,
                email,
                contract
            FROM
                customer
            """)
    items = cur.fetchall()

    # タスク情報
    cur.execute("""
            SELECT
                *
            FROM
                task
            WHERE
                progress NOT IN ("完了")
                AND deleted_at IS NULL
            ORDER BY
                deadline ASC
            """)
    tasks = cur.fetchall()
    con.close()

    return render_template("customer.html",id=id,items=items, tasks=tasks)


@app.route("/archived_customer")
def archived_customer_page():
    # DBから企業一覧を取り出す
    filepath = "database/app.db"
    con = sqlite3.connect(filepath)
    cur = con.cursor()
    # この中でクエリを書く
    # 解約済み顧客情報
    cur.execute("""
            SELECT
                customer_id,
                company,
                address,
                tel,
                email,
                contract
            FROM
                customer
            WHERE
                contract IN ('解約済み')
            """)
    items = cur.fetchall()
    con.close()

    return render_template("archived_customer.html",items=items)


@app.route("/add_customer", methods=["GET","POST"])
def add_customer_page():
    form = AddCustomerForm(request.form)
    # POST
    if request.method == "POST":
        # 会社名
        company = form.company.data
        # 住所
        address = form.address.data
        # お電話番号
        tel = form.tel.data
        # メールアドレス
        email = form.email.data

        # 契約状況
        contract = form.contract.data

        # DBに顧客情報を追加する
        filepath = "database/app.db"
        # databaseにレコードを追加
        con = sqlite3.connect(filepath)
        cur = con.cursor()
        cur.execute('INSERT INTO customer (company, address, tel, email, contract) VALUES (?, ?, ?, ?, ?)',
                    (company, address, tel, email, contract))
        con.commit()
        con.close()

        # データ出力
        return render_template("success_add_customer.html",company=company,address=address,tel=tel,email=email,contract=contract)
    # GET
    else:
        return render_template("add_customer.html", form=form)

# ▼▼▼---ココに、タスク追加をするページを作成してみよう！---▼▼▼
@app.route("/add_task-<int:customer_id>", methods=["GET","POST"])
def add_task_page(customer_id):
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
        filepath = "database/app.db"
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
                               progress=progress
                               )
    # GET
    else:
        return render_template("add_task.html", form=form, customer_id=customer_id)
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
        filepath = "database/app.db"
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
        # DBから企業一覧を取り出す
        filepath = "database/app.db"
        con = sqlite3.connect(filepath)
        cur = con.cursor()
        # この中でクエリを書く
        # タスク更新情報
        cur.execute(f"""
                SELECT
                    *
                FROM
                    task
                WHERE
                    task_id = {task_id}
                    AND deleted_at IS NULL
                """)
        task_update = cur.fetchall()
        print(task_update)
        return render_template("update_task.html", form=form, task_id=task_id, task_update=task_update)

@app.route("/delete_task-<int:task_id>")
def delete_task_page(task_id):
    # DBに顧客情報を追加する
    filepath = "database/app.db"
    # databaseにレコードを追加
    con = sqlite3.connect(filepath)
    cur = con.cursor()
    cur.execute(f"""
                UPDATE
                    task
                SET
                    deleted_at = datetime('now', '+9 hours')
                WHERE
                    task_id = {task_id}
                """)
    con.commit()
    con.close()
    return redirect(url_for("task_view_page"))


@app.route("/deleted_task")
def deleted_task_page():
    #DBからタスク一覧を取り出す
    filepath = "database/app.db"
    con = sqlite3.connect(filepath)
    cur = con.cursor()
    # この中でクエリを書く
    # タスクを削除する
    cur.execute("""
            SELECT
                * 
            FROM
                task
            WHERE
                deleted_at IS NOT NULL 
            ORDER BY
                deleted_at DESC
            """)
    tasks = cur.fetchall()
    con.close()

    return render_template("deleted_task.html" , tasks = tasks)

@app.route("/restore_task-<int:task_id>")
def restore_task_page(task_id):
    # DBに顧客情報を追加する
    filepath = "database/app.db"
    # databaseにレコードを追加
    con = sqlite3.connect(filepath)
    cur = con.cursor()
    # タスクを復元するクエリ
    cur.execute(f"""
                UPDATE
                    task
                SET
                    deleted_at = NULL
                WHERE
                    task_id = {task_id}
                """)
    con.commit()
    con.close()
    return redirect(url_for("deleted_task_page"))

@app.route("/update_customer-<int:customer_id>", methods=["GET","POST"])
def update_customer_page(customer_id):
    form = AddCustomerForm(request.form)
    # POST
    if request.method == "POST":
        # 会社名
        company = form.company.data
        # 住所
        address = form.address.data
        # お電話番号
        tel = form.tel.data
        # メールアドレス
        email = form.email.data

        # 契約状況（新たな顧客登録なので強制的に1となる）
        contract = form.contract.data
        
        # DBに顧客情報を追加する
        filepath = "database/app.db"
        # databaseにレコードを追加
        con = sqlite3.connect(filepath)
        cur = con.cursor()
        # タスクが残っている状態で”解約済み”に出来ないようにするコード（アラート付き）、それ以外の場合は変更可
        if contract == "解約済み":
            cur.execute(f"""
                        SELECT
                            count(*)
                        FROM
                            task
                        WHERE
                            progress NOT IN ('完了')
                            AND customer_id = {customer_id}
                            AND deleted_at IS NULL
                        """)
            output = cur.fetchall()
            print(output)
            if output[0][0] == 0:
                cur.execute(f"""
                            UPDATE
                                customer
                            SET
                                contract=?
                            WHERE
                                customer_id = ?
                            """,
                            (contract, customer_id))
                con.commit()
                con.close()            
            else:
                flash('まだこちらのお客様のタスクが残っています。')
                flash('すべてのタスクを完了にしてから更新してください。')
        else:
            cur.execute("""UPDATE
                                customer
                            SET
                                company=?,
                                address=?,
                                tel=?,
                                email=?,
                                contract=?
                            WHERE
                                customer_id=?
                            """,
                        (company, address, tel, email, contract, customer_id))
            con.commit()
            con.close()
        return redirect(url_for("customer_list_page"))
    # GET
    else:
        # DBから企業一覧を取り出す
        filepath = "database/app.db"
        con = sqlite3.connect(filepath)
        cur = con.cursor()
        # この中でクエリを書く
        # タスク更新情報
        cur.execute(f"""
                SELECT
                    *
                FROM
                    customer
                WHERE
                    customer_id = {customer_id}
                """)
        update_customer = cur.fetchall()
        return render_template("update_customer.html", form=form, customer_id=customer_id, update_customer=update_customer)


# 404エラーが発生した場合の処理
@app.errorhandler(404)
def error_404(error): # errorは消さない！
    return render_template('404.html')

if __name__ == "__main__":
    app.run(debug=True)