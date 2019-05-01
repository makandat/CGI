#!/usr/bin/env python3
#!C:\Program Files (x86)\Python37\python.exe
# -*- code=utf-8 -*-
# Music テーブルのマーク種別
#   MySQL を利用
from WebPage import WebPage
from MySQL import MySQL

# CGI WebPage クラス
class MainPage(WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.__mysql = MySQL()
    self.setPlaceHolder('message', "")
    self.setPlaceHolder('marks', self.getMarks())
    return

  # マーク一覧を得る。
  def getMarks(self) :
    rows = self.__mysql.query("SELECT DISTINCT mark FROM Music")
    buff = ""
    for row in rows :
      if row[0] == None :
        continue
      buff += WebPage.tag("option", row[0])
      buff += "\n"
    return buff

# メイン開始位置
wp = MainPage('templates/mark.html')
wp.echo()
