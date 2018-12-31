#!/usr/bin/env python3
#  ユーザ管理ログイン
from WebPage import WebPage;

class LogoutPage(WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.cookie('userid', '')


# 開始
wp = LogoutPage('templates/Logout.html')
wp.echo()
