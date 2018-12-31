#!/usr/bin/env python3
#  ユーザ管理 パスワード更新
from WebPage import WebPage
from Users import Users

class NewUserPage(WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    if 'userid' in self.cookies.keys() :
      if 'userid' in self.params.keys() :
        # POST
        self.users = Users()
        self.users.update_password(self.params['userid'].value, self.params['password'].value)
        self.vars['message'] = self.params['userid'].value + " のパスワードを更新しました。"
      else :
        # GET
        self.vars['message'] = ""
    else :
      self.redirect('Logout.cgi', 0)


# 開始
wp = NewUserPage('templates/update_password.html')
wp.echo()
