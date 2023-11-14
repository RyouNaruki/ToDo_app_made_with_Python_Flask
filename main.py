from flask import Flask
from flask import render_template
from flask import request
import os
import sqlite3

app = Flask(__name__)


from forms import UserInfoForm


# データベースにデータを追加する関数
def add_data_to_database(name,company,tel,email):
    # databaseにレコードを追加
    con = sqlite3.connect('database/customer.db')
    cur = con.cursor()
    cur.execute('INSERT INTO customer (name, company, tel, email) VALUES (?, ?, ?, ?)',
                (name, company, tel, email))
    con.commit()
    con.close()


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
        # お名前
        name = form.name.data
        # 会社名
        company = form.company.data
        # お電話番号
        tel = form.tel.data
        # メールアドレス
        email = form.email.data
        # 実行環境で条件分岐をする
        if os.getenv('GAE_ENV', '').startswith('standard'): # True = cloud, False = local
            # クラウド環境の場合
            from google.cloud import storage
            # GCS上のdbを取得する
            client = storage.Client()
            bucket_name = "todo-app-405104.appspot.com"
            bucket = client.get_bucket(bucket_name)
            blob_name = "customer.db"
            blob = bucket.blob(blob_name)
            blob.download_to_filename('/tmp/customer.db')

            # データベースにデータを追加する
            add_data_to_database(name,company,tel,email)

            #dbを上書きする
            blob.upload_from_filename('/tmp/customer.db')

            return render_template("success.html",name=name,company=company,tel=tel,email=email)
        else:
            # ローカル環境の場合
            # データベースにデータを追加する
            add_data_to_database(name,company,tel,email)
            return render_template("success.html",name=name,company=company,tel=tel,email=email)

    # GET
    else:
        return render_template("add_customer.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)