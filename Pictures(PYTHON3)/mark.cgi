#!/usr/bin/python3
#!C:\Program Files (x86)\Python37\python.exe
# -*- code=utf-8 -*-
# Pictures テーブルのマーク種別
#   MySQL を利用
import WebPage as page
import FileSystem as fsys
import MySQL

# CGI WebPage クラス
class MainPage(page.WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.__mysql = MySQL.MySQL()
    self.setPlaceHolder('message', "")
    self.setPlaceHolder('marks', self.getMarks())
    return

  # マーク一覧を得る。
  def getMarks(self) :
    rows = self.__mysql.query("SELECT DISTINCT mark FROM Pictures")
    buff = ""
    for row in rows :
      if row[0] == None :
        continue
      buff += page.WebPage.tag("option", row[0])
      buff += "\n"
    return buff

# メイン開始位置
wp = MainPage('templates/mark.html')
wp.echo()
