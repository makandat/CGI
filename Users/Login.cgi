#!/usr/bin/env python3
#  ユーザ管理ログイン
from WebPage import WebPage;
from Users import Users

class LoginPage(WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    if 'userid' in self.params.keys() :
      # Post Back
      self.users = Users()
      if 'userid' in self.params.keys() == False or 'password' in self.params.keys() == False :
        self.vars['message'] = '<span style="color:red">エラー：ログインできませんでした。</span>'
      elif self.users.authorize(self.params['userid'].value, self.params['password'].value) :
        self.vars['message'] = '<a href="/cgi-bin/Users/IndexUsers.cgi">ログインしました。ここをクリック</a>'
        self.cookie('userid', self.params['userid'].value)
        # self.redirect('/cgi-bin/Users/IndexUsers.cgi')  # クッキーが送信されない。
      else :
        self.vars['message'] = '<span style="color:red">エラー：ログインできませんでした。</span>'
    else :
      self.vars['message'] = ''



# 開始
wp = LoginPage('templates/Login.html')
wp.echo()
