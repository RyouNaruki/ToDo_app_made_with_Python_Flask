from wtforms import Form
#電話番号のフィールドのインポート
from wtforms.fields import TelField

from wtforms.fields import (
    StringField, SubmitField,IntegerField,DateField,SelectField
)
# python3.11以上の場合
#from wtforms.fields.html5 import EmailField
#wtforms.fields.html5.TelField
#python 3.11未満の場合
from wtforms.fields import EmailField

from wtforms.validators import (
    DataRequired, Email, EqualTo
)


# 顧客追加フォーム
class AddCustomerForm(Form):
    # 会社名：文字列入力
    company = StringField("会社名", validators=[DataRequired('この項目は必須入力です。')], render_kw={"placeholder":"〇〇〇〇株式会社"})
    # お電話番号：文字列入力
    tel  = TelField("電話番号",validators=[DataRequired('この項目は必須入力です。')], render_kw={"placeholder":"012-3456-7890"})
    # メールアドレス：メールアドレス入力
    email = EmailField("メールアドレス", render_kw={"placeholder":"xxxx@example.com"}, validators=[EqualTo("confirm_password", "メールアドレスが一致しません"), DataRequired('この項目は必須入力です。')])
    # メールアドレス(確認用)：メールアドレス入力
    confirm_email = EmailField("メールアドレス確認", render_kw={"placeholder":"xxxx@example.com"}, validators=[Email("メールアドレスのフォーマットではありません"), DataRequired('この項目は必須入力です。')])
    
    # ボタン
    submit = SubmitField("送信")

# ▼▼▼タスク追加フォームの型を作ってみよう▼▼▼
class AddTaskForm(Form):
    #会社の情報を引っ張ってくる（後々制作）：数値入力
    customer_id = IntegerField("顧客ID: ", render_kw={"placeholder":"〇〇〇〇"})
    #相手方担当者：文字列入力
    sir = StringField("先方の担当者様: ", render_kw={"placeholder":"山田太郎"})
    #タスク説明：文字列入力
    task_content = StringField("タスクの内容: ", render_kw={"placeholder":"届出"})
    #期日：日付入力
    deadline = DateField("期日: ", render_kw={"placeholder":"2023-12-31"})
    #担当者：セレクトボックス, PIC=Person In Change
    pic = SelectField("担当者: ", choices=[
                                            ("稲垣大輔"),
                                            ("関幸子"), 
                                            ("濱野竜聖"),
                                            ("成木涼雨"),
                                            ("宇佐美ささ波")
                                            ])
    #タスクの進捗状況：セレクトボックス
    progress = SelectField("タスクの進捗状況: ", choices=[
                                                        ( "未着手"),
                                                        ("進行中"), 
                                                        ("完了")
                                                        ])

    # ボタン
    submit = SubmitField("送信")
# ▲▲▲タスク追加フォームの型を作ってみよう▲▲▲