#!/usr/bin/env python3
#  ユーザ管理 新規ユーザ登録
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
        self.users.add_new(self.params['userid'].value, self.params['password'].value, self.params['info'].value)
        self.vars['message'] = self.params['userid'].value + " を登録しました。"
      else :
        # GET
        self.vars['message'] = ""
    else :
      self.redirect('Logout.cgi', 0)


# 開始
wp = NewUserPage('templates/add_new.html')
wp.echo()
