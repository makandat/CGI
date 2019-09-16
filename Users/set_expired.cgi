#!/usr/bin/env python3
#  ユーザ管理 ユーザ有効期限を無効にする。
from WebPage import WebPage
from Users import Users

class ExpireUserPage(WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    userc = self.getCookie('userid', '')
    if userc == "" :
      self.redirect('Logout.cgi', 0)
    self.setPlaceHolder("userc", userc)
    # ユーザ一覧を得る。
    self.users = Users()
    self.listUsers()
    if self.getMethod() == 'POST' :
      # POST
      userp = self.getParam('users')
      if self.users.isValidUser(userp, userc, 4) :
        self.expire(self.getParam('users'))
        self.setPlaceHolder('message', userp + " を無効にしました。")
      else :
        self.setPlaceHolder('message', "不正な操作です。(管理者のみが可能)")
    else :
      # GET
      self.setPlaceHolder('message', "")

  # ユーザの無効化
  def expire(self, userid) :
    self.users.set_expired(userid)
    return

  # ユーザ一覧を得る。
  def listUsers(self) :
    buff = ""
    rows = self.users.query("SELECT userid FROM Users ORDER BY userid")
    for row in rows :
      buff += "<option>"
      buff += row[0]
      buff += "</option>\n"
    self.setPlaceHolder('options', buff)
    return

# 開始
wp = ExpireUserPage('templates/set_expired.html')
wp.echo()
