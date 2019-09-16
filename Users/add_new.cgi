#!/usr/bin/env python3
#  ユーザ管理 新規ユーザ登録
from WebPage import WebPage
from Users import Users

class NewUserPage(WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    userc = self.getCookie('userid', '')
    self.setPlaceHolder("userc", userc)
    if userc == "" :
      self.redirect('Logout.cgi', 0)
    self.users = Users()
    if self.getMethod() == "POST" :
      # POST
      if self.users.isValidUser(userc, userc, 3) :
        userp = self.getParam('userid')
        if self.users.exists(userp) :
          self.setPlaceHolder('message', "エラー：すでに登録されています。")
          return
        self.users.add_new(userp, self.getParam('password'), self.getParam('info'))
        self.setPlaceHolder('message', userp + " を登録しました。")
      else :
        self.setPlaceHolder('message', "エラー：不正な操作です。(管理者のみが可能)")
    else :
      # GET
      self.setPlaceHolder('message', "")


# 開始
wp = NewUserPage('templates/add_new.html')
wp.echo()
