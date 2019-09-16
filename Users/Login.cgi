#!/usr/bin/env python3
#  ユーザ管理ログイン  v1.10  2019-09-15
import WebPage
import Users

class LoginPage(WebPage.WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.setPlaceHolder("style", "")
    if self.isParam('userid') :
      # Post Back
      self.users = Users.Users()
      userid = self.getParam("userid", "")
      password = self.getParam("password", "")
      if self.isParam('userid') == False or self.isParam('password') == False :
        self.setPlaceHolder('message', '<span style="color:red">エラー：ログインできませんでした。</span>')
      elif self.users.authorize(userid, password) :
        self.setPlaceHolder("style", ' style="display:none;"')
        self.setPlaceHolder('message', '<a href="/cgi-bin/Users/IndexUsers.cgi">ログインしました。ここをクリック</a>')
        self.cookie('userid', userid)
      else :
        self.setPlaceHolder('message', '<span style="color:red">エラー：ログインできませんでした。</span>')
    else :
      self.setPlaceHolder('message', '')



# 開始
wp = LoginPage('templates/Login.html')
wp.echo()
