#!/usr/bin/env python3
#!C:\Program Files (x86)\Python37\python.exe
# -*- code=utf-8 -*-
#   index.cgi  Version 1.00
from WebPage import WebPage
from MySQL import MySQL
import FileSystem as fs
import Common
#from syslog import syslog

VERSION = "1.0"
LIMIT = 200

# CGI WebPage クラス
class MainPage(WebPage) :

  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.__mysql = MySQL()
    self.setPlaceHolder('title', '画像アルバム ' + VERSION)
    self.setPlaceHolder('message', '')
    self.showAlbums()
    return

  # アルバム一覧を表示する。
  def showAlbums(self) :
    sql = "SELECT id, name, 0, mark, info, bindata FROM Album ORDER BY id"
    rows = self.__mysql.query(sql)
    if len(rows) == 0 :
      self.setPlaceHolder('message', 'アルバムが登録されていません。')
      self.setPlaceHolder('content', '')
    else :
      content = ""
      for row in rows :
        tr = "<tr>"
        id = row[0]
        name = row[1]
        tr += WebPage.tag('td', id, "style='text-align:center;'")   # id
        tr += WebPage.tag('td', f"<a href=\"show_items.cgi?id={id}\">{name}</a>")  # name
        n = self.__mysql.getValue(f"SELECT COUNT(album) FROM PictureAlbum GROUP BY album HAVING album={id}")
        if n == None :
          n = 0
        tr += WebPage.tag('td', n, "style='text-align:right;'")  # summation
        tr += WebPage.tag('td', row[3])  # mark
        tr += WebPage.tag('td', row[4])  # info
        bindata = row[5]
        if bindata == None or bindata == 0 :
          tr += WebPage.tag('td', '')  # 無効なbindata
        else :
          tr += WebPage.tag('td', f"<img src=\"extract.cgi?id={bindata}\" alt=\"{bindata}\" />")  # bindata
        tr += "</tr>\n"
        content += tr
      self.setPlaceHolder('content', content)
    return
        
# 実行開始
wp = MainPage('templates/index.html')
wp.echo()
