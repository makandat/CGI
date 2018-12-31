#!/usr/bin/env python3
#  ユーザ管理 新規ユーザ登録
from WebPage import WebPage
from Users import Users

class ExpireUserPage(WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    if 'userid' in self.cookies.keys() :
      # ユーザ一覧を得る。
      self.__users = Users()
      self.listUsers()
      if 'users' in self.params.keys() :
        # POST
        self.expire(self.params['users'].value)
        self.vars['message'] = self.params['users'].value + " を無効にしました。"
      else :
        # GET
        self.vars['message'] = ""
    else :
      self.redirect('Logout.cgi', 0)

  # ユーザの無効化
  def expire(self, userid) :
    self.__users.set_expired(userid)

  # ユーザ一覧を得る。
  def listUsers(self) :
    buff = ""
    rows = self.__users.query("SELECT userid FROM Users ORDER BY userid")
    for row in rows :
      buff += "<option>"
      buff += row[0]
      buff += "</option>\n"
    self.vars['options'] = buff

# 開始
wp = ExpireUserPage('templates/set_expired.html')
wp.echo()
