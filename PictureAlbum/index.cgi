#!C:\Program Files (x86)\Python37\python.exe
#!/usr/bin/env python3
# -*- code=utf-8 -*-
#   index.cgi  Version 1.50  2020-03-07
from WebPage import WebPage
from MySQL import MySQL
import FileSystem as fs
import Common
import Text
#from syslog import syslog

VERSION = "1.50"
LIMIT = 200

# CGI WebPage クラス
class MainPage(WebPage) :

  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.__mysql = MySQL()
    self.setPlaceHolder('title', '画像アルバム ' + VERSION)
    self.setPlaceHolder('message', '')
    # グループ名一覧取得
    self.getGroupNames()
    # グループ名パラメータ取得と設定
    if self.isParam("groupname") :
      self.groupname = self.getParam("groupname")
      self.setCookie('groupname', self.groupname)
    else :
      if self.isCookie('groupname') :
        self.groupname = self.getCookie('groupname')
      else :
        self.groupname = 'ALL'
        self.setCookie('groupname', 'ALL')
    # アルバム内容を表示
    self.showAlbums()
    return

  # アルバム一覧を表示する。
  def showAlbums(self) :
    if self.groupname == "ALL" :
      sql = "SELECT id, name, 0, mark, info, bindata, groupname, `date` FROM Album WHERE mark='picture' ORDER BY id"
    elif self.groupname == "NONAME" :
      sql = "SELECT id, name, 0, mark, info, bindata, groupname, `date` FROM Album WHERE mark='picture' AND ISNULL(groupname) ORDER BY id"
    else :
      sql = f"SELECT id, name, 0, mark, info, bindata, groupname, `date` FROM Album WHERE mark='picture' AND groupname = '{self.groupname}' ORDER BY id"
    rows = self.__mysql.query(sql)
    if len(rows) == 0 :
      self.setPlaceHolder('message', 'アルバムが登録されていません。')
      self.setPlaceHolder('content', '')
    else :
      content = "<tr><th>アルバム番号</th><th>アルバム名</th><th>収録数</th><th>種別</th><th>情報</th><th>イメージ</th><th>グループ名</th><th>更新日</th></tr>\n"
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
        if groupName == None :
          groupName = ''
        tr += WebPage.tag('td', groupName)
        udate = row[7] # date
        if udate == None :
          udate = ""
        tr += WebPage.tag('td', udate)
        tr += "</tr>\n"
        content += tr
      self.setPlaceHolder('content', content)
    return


  # グループ名一覧取得
  def getGroupNames(self) :
    sql = "SELECT DISTINCT groupname FROM album"
    s = ""
    rows = self.__mysql.query(sql)
    for row in rows :
      gn = str(row[0])
      if gn == "" or gn == None :
        pass
      else :
        s += "<option>"
        s += gn
        s += "</option>\n"
    self.setPlaceHolder("groupnames", s)
    return

# 実行開始
wp = MainPage('templates/index.html')
wp.echo()
