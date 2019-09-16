#!/usr/bin/env python3
#  ユーザ管理 ユーザ情報修正
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
    if self.users.isValidUser(userc, userc, 2) :
      if self.getMethod() == "POST" :
        # POST
        userp = self.getParam('userid')
        self.users.modify_info(userp, self.getParam('info'))
        self.embed({"message":userp + " の情報を修正しました。", "userc":userc})
      else :
        # GET
        self.embed({"message":"", "userc":userc})
    else :
      self.embed({"message":"エラー：不正な操作です。(管理者のみが可能)", "userc":userc})


# 開始
wp = NewUserPage('templates/modify_info.html')
wp.echo()
