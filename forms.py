from wtforms import Form

from wtforms.fields import (
    StringField, SubmitField
)
# python3.11以上の場合
from wtforms.fields.html5 import EmailField
#python 3.11未満の場合
#from wtforms.fields import EmailField

from wtforms.validators import (
    DataRequired, Email, EqualTo
)


# 顧客追加フォーム
class AddCustomerForm(Form):
    # 年齢：静数値入力
    company = StringField("会社名", render_kw={"placeholder":"〇〇〇〇株式会社"})
    # お電話番号：文字列入力
    tel = StringField("電話番号",render_kw={"placeholder":"012-3456-7890"})
    # メールアドレス：メールアドレス入力
    email = EmailField("メールアドレス", render_kw={"placeholder":"xxxx@example.com"}, validators=[EqualTo("confirm_password", "メールアドレスが一致しません")])
    # メールアドレス(確認用)：メールアドレス入力
    confirm_email = EmailField("メールアドレス確認", render_kw={"placeholder":"xxxx@example.com"}, validators=[Email("メールアドレスのフォーマットではありません")])
    # ボタン
    submit = SubmitField("送信")

# ▼▼▼タスク追加フォームの型を作ってみよう▼▼▼

# ▲▲▲タスク追加フォームの型を作ってみよう▲▲▲