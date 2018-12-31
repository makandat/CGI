#!/usr/bin/env python3
#  ユーザ管理 ユーザ一覧とメニュー
from WebPage import WebPage;
from Users import Users

class IndexUsers(WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    if 'userid' in self.cookies :
      self.__users = Users()
      self.vars['table'] = self.__users.userlist(all=True)
    else :
      self.redirect('/cgi-bin/Users/Login.cgi')


# 開始
wp = IndexUsers('templates/IndexUsers.html')
wp.echo()
