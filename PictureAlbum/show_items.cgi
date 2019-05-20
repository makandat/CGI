#!/usr/bin/env python3
#!C:\Program Files (x86)\Python37\python.exe
# -*- code=utf-8 -*-
#   show_items.cgi 2019-05-20
from WebPage import WebPage
from MySQL import MySQL
import FileSystem as fs
import Common
#from syslog import syslog

LIMIT = 200

# CGI WebPage クラス
class MainPage(WebPage) :

  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    Common.init_logger('C:/temp/Logger.log')
    self.__mysql = MySQL()
    self.setPlaceHolder('message', '')
    self.setPlaceHolder('title', '全登録画像一覧')
    if self.isParam('id') :
      id = int(self.getParam('id'))
      self.setPlaceHolder('album', id)
      self.setPlaceHolder('display', '')
      self.showPictures(id, self.isParam('pictures'))
    else :
      self.setPlaceHolder('display', 'display:none;')
      self.showPictures()
    return

  # 画像一覧を表示する。
  def showPictures(self, id=0, picture=False) :
    sql = "SELECT P.id, P.album, P.title, P.path, P.creator, P.info, P.fav, P.bindata, A.name FROM PictureAlbum P INNER JOIN Album A ON A.id=P.album"
    if id > 0 :
      sql += f" WHERE album={id}"
    rows = self.__mysql.query(sql)
    if len(rows) == 0 :
      self.setPlaceHolder('message', '画像情報が登録されていません。')
      self.setPlaceHolder('content', '')
      return
    content = ""
    pictures = ""
    if picture :
      self.setPlaceHolder('table1', 'display:none;')
    for row in rows :
      if picture :
        pictures += "<div style=\"margin-bottom:16px;\"><img src=\"getImage.cgi?path={0}\" /><br />{0}</div>".format(row[3])
      else :
        tr = "<tr>"
        tr += WebPage.tag("td", row[0])  # id
        album = str(row[1]) + " (" + row[8] + ")"
        tr += WebPage.tag("td", album)  # album
        tr += WebPage.tag("td", row[2])  # title
        tr += WebPage.tag("td", MainPage.makeLink(row[3]))  # path
        tr += WebPage.tag("td", row[4])  # creator
        tr += WebPage.tag("td", row[5])  # info
        tr += WebPage.tag("td", row[6])  # fav
        tr += WebPage.tag("td", row[7])  # bindata
        tr += "</tr>\n"
        content += tr
    self.setPlaceHolder('content', content)
    self.setPlaceHolder('pictures', pictures)
    if id > 0 :
      albumName = self.getAlbumName(id)
      self.setPlaceHolder('title', 'アルバム#' + str(id) + ' "' + albumName + '"画像一覧')
    else :
      self.setPlaceHolder('title', '全アルバム画像一覧')
    return

  # アルバム番号から名称を得る。
  def getAlbumName(self, id) :
    sql = f"SELECT name FROM Album WHERE id={id}"
    name = self.__mysql.getValue(sql)
    return name

  # パスからリンクを作る
  @staticmethod
  def makeLink(path) :
    anchor = f"<a href=\"getImage.cgi?path={path}\" target=\"_blank\">{path}</a>"
    return anchor



# 実行開始
wp = MainPage('templates/show_items.html')
wp.echo()
