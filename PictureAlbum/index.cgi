#!/usr/bin/env python3
#!C:\Program Files (x86)\Python37\python.exe
# -*- code=utf-8 -*-
#   index.cgi  Version 1.25  2020-02-26
from WebPage import WebPage
from MySQL import MySQL
import FileSystem as fs
import Common
import Text
#from syslog import syslog

VERSION = "1.25"
LIMIT = 200

# CGI WebPage クラス
class MainPage(WebPage) :

  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.__mysql = MySQL()
    self.setPlaceHolder('title', '画像アルバム ' + VERSION)
    self.setPlaceHolder('message', '')
    # アイコン・詳細表示設定
    self.setPlaceHolder('view', 'detail')
    if self.isCookie('view') :
      self.view = self.getCookie('view')
      self.setPlaceHolder('view', 'icons' if self.view == 'detail' else 'detail')
    else :
      self.view = 'detail'
      self.setCookie('view', 'detail')
    # アルバム内容を表示
    if self.isParam('view') :
      view = self.getParam('view')
      if view == 'icons' :
        self.setCookie('view', 'icons')
        self.view = 'icons'
        self.setPlaceHolder('view', 'detail')
        # アルバム一覧をアイコン表示する。
        self.showIcons()
      else :
        self.setCookie('view', 'detail')
        self.view = 'detail'
        self.setPlaceHolder('view', 'icons')       
        # アルバム一覧を詳細表示する。
        self.showAlbums()
    else :
      self.view = "detail"
      self.setCookie('view', 'detail')
      self.showAlbums()
    return

  # アルバム一覧を表示する。
  def showAlbums(self) :
    sql = "SELECT id, name, 0, mark, info, bindata, groupname FROM Album WHERE mark='picture' ORDER BY id"
    rows = self.__mysql.query(sql)
    if len(rows) == 0 :
      self.setPlaceHolder('message', 'アルバムが登録されていません。')
      self.setPlaceHolder('content', '')
    else :
      content = "<tr><th>アルバム番号</th><th>アルバム名</th><th>収録数</th><th>種別</th><th>情報</th><th>イメージ</th><th>グループ名</th></tr>\n"
      for row in rows :
        tr = "<tr>"
        id = row[0]
        name = row[1]
        tr += WebPage.tag('td', id, "style='text-align:center;'")   # id
        tr += WebPage.tag('td', f"<a href=\"show_items.cgi?id={id}&pictures=1\" target=\"_blank\">{name}</a>")  # name
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
        groupName = row[6]  # groupname
        tr += WebPage.tag('td', groupName)
        if groupName == None :
          groupName = ''
        
        tr += "</tr>\n"
        content += tr
      self.setPlaceHolder('content', content)
    return

  # アルバム一覧をアイコンで表示する。
  def showIcons(self) :
    sql = "SELECT id, name, 0, mark, info, bindata, picturesid FROM Album WHERE mark='picture' ORDER BY id"
    rows = self.__mysql.query(sql)
    if len(rows) == 0 :
      self.setPlaceHolder('message', 'アルバムが登録されていません。')
      self.setPlaceHolder('content', '')
    else :
      content = "<div>\n"
      for row in rows :
        id = row[0]
        name = row[1]
        bindata = row[5]
        content += "<div style=\"display:inline-block;width:15%;\">"
        if bindata == None or bindata == 0 :
          img = "<img src=\"/img/NoImage.jpg\" />"
        else :
          img = f"<img src=\"extract.cgi?id={bindata}\" />"
          imglink = WebPage.tag('a', img, f"href=\"show_items.cgi?id={id}\"")
        content += WebPage.tag('div', imglink, "style=\"text-align:center;\"")
        content += WebPage.tag('div', Text.left(name, 18), "style=\"font-size:10pt;\"")
        content += "</div>\n"
      content += "</div>\n"
      self.setPlaceHolder('content', content)
    return
        
# 実行開始
wp = MainPage('templates/index.html')
wp.echo()
