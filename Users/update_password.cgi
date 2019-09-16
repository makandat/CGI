#!/usr/bin/env python3
#  ユーザ管理 パスワード更新
from WebPage import WebPage
from Users import Users

class NewUserPage(WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.users = Users()
    userc = self.getCookie('userid', '')
    if userc == "" :
      self.redirect('Logout.cgi', 0)     
    if self.getMethod() == "POST" :
      # POST
      userp = self.getParam('userid', '')
      if self.users.isValidUser(userp, userc, 1) :
        password = self.getParam('password')
        if len(password) < 5 :
          self.setPlaceHolder('message', "エラー：パスワードが短すぎます。")
          return
        self.users.update_password(userp, password)
        self.setPlaceHolder('message', userp + " のパスワードを更新しました。")
      else :
        self.setPlaceHolder('message', "エラー：不正な操作です。")
    else :
      # GET
      self.setPlaceHolder('message', "")


# 開始
wp = NewUserPage('templates/update_password.html')
wp.echo()
