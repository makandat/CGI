#!/usr/bin/python3
# reset_password.py
#  Users テーブルのパスワードをリセットする。(ユーザ名と同じにする)
import Common
import Users

if Common.count_args() == 0 :
  Common.stop(9, "パラメータとしてユーザIDを指定してください。")

userid = Common.args(0)
users = Users.Users()
users.update_password(userid, userid)
Common.esc_print("yellow", "パスワードをリセットしました。パスワードはユーザIDと同じになっています。")

