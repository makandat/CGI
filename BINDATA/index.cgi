#!/usr/bin/env python3
#!C:\Program Files (x86)\Python37\python.exe
#  BINDATA バイナリファイル index.cgi  2019-05-08
from WebPage import WebPage
import Text
from MySQL import MySQL
import FileSystem as fs
#from syslog import syslog

SELECT = "SELECT id, title, original, datatype, info, size FROM BINDATA"

class BinDataPage(WebPage) :
  LIMIT = 100
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.__mysql = MySQL()
    # 表示順を得る。
    self.order = self.getCookie('order', 'ASC')
    # 前回の表示位置を得る。
    self.idl = self.getCookie('idl', '0')
    # 表示方法の初期値
    self.view = "detail"
    # 表示順の指定
    if self.isParam('order') :
      if self.order == 'DESC' :
        self.order = "ASC"
        self.setCookie('order', 'ASC')
      else :
        self.order = "DESC"
        self.setCookie('order', 'DESC')
      self.showContent()
    # フィルタの指定
    elif self.isParam('filter') :
      filter = self.getParam('filter')
      if filter == "image" :
        # 画像
        where = " WHERE datatype='.jpg' OR datatype='.png' OR datatype='.gif'"
        self.showContent(where)
      elif filter == "audio" :
        # 音声
        where = " WHERE datatype='.wav' OR datatype='.mp4' OR datatype='.m4a'"
        self.showContent(where)
      elif filter == "zip" :
        # 圧縮ファイル
        where = " WHERE datatype='.zip' OR datatype='.gz' OR datatype='.bz2'"
        self.showContent(where)
      else :
        self.setPlaceHolder('content', "<tr><td>不正なパラメータ</td></tr>")
        self.setPlaceHolder('images', "")
    # ページの指定
    elif self.isParam('id') :
      id = self.getParam('id')
      if id == "first" :
        # 先頭
        where = ""
      elif id == "prev" :
        # 前
        if self.order == "ASC" :
          where = " WHERE id > " + str(int(self.idl) - BinDataPage.LIMIT * 2)
        else :
          where = " WHERE id < " + str(int(self.idl) + BinDataPage.LIMIT * 2)
      elif id == "next" :
        # 次
        if self.order == "ASC" :
          where = " WHERE id > " + self.idl
        else :
          where = " WHERE id < " + self.idl
      elif id == "last" :
        # 最後
        if self.order == "ASC" :
          idmax = self.getMaxId()
          where = " WHERE id > " + str(idmax - BinDataPage.LIMIT)
        else :
          idmin = self.getMinId()
          where = " WHERE id < " + str(idmin + BinDataPage.LIMIT)
      else :
        # id 設定
        if self.order == "ASC" :
          where = " WHERE id >= " + id
        else :
          where = " WHERE id <= " + id
      if self.view == "detail" :
        self.showContent(where)
      else :
        self.showIcons(where)
    # 表示方法
    elif self.isParam('view') :
      self.view = self.getParam('view')
      self.setCookie('view', self.view)
      self.setPlaceHolder('view', "icons" if self.view == "detail" else "detail")
      if self.view == "detail" :
        self.showContent()
      else :
        self.showIcons()
    # デフォルトの表示
    else :
      self.showContent()
    return

  # BINDATA テーブルの内容一覧を得る。
  def showContent(self, where="") :
    buff = "<tr><th>id</th><th>タイトル</th><th>オリジナルファイル</th><th>ファイルタイプ</th><th>情報</th><th>サイズ</th></tr>\n"
    orderby = " ORDER BY id " + self.order
    sql = SELECT + where + orderby + " LIMIT " + str(BinDataPage.LIMIT)
    rows = self.__mysql.query(sql)
    for row in rows :
      id = str(row[0])
      title = row[1]
      original = "" if row[2] == None else row[2].replace("\\", "/")
      datatype = row[3]
      info = "" if row[4] == None else row[4]
      size = "" if row[5] == None else row[5]
      buff += "<tr>"
      buff += f"<td><a href=\"modify.cgi?id={id}\">{id}</a></td>"
      buff += f"<td><a href='extract.cgi?id={id}' target='_blank'>{title}</a></td><td>{original}</td><td>{datatype}</td><td>{info}</td><td>{size}</td>"
      buff += "</tr>\n"
      self.idl = id
    self.setCookie('idl', self.idl)
    self.setPlaceHolder('content', buff)
    self.setPlaceHolder('images', "")
    return

  # アイコン表示
  def showIcons(self, where="") :
    images = "<div>"
    sql = SELECT + where + " AND (datatype='.jpg' OR datatype='.png' OR datatype='.gif') LIMIT " + str(BinDataPage.LIMIT)
    if where == "" :
      sql = SELECT + " WHERE datatype='.jpg' OR datatype='.png' OR datatype='.gif' LIMIT " + str(BinDataPage.LIMIT)
    rows = self.__mysql.query(sql)
    for row in rows :
      id = str(row[0])
      title = row[1]
      title1 = Text.left(title, 16)
      images += "<div style='display:inline-block;padding:6px;'>"
      images += f"<img src=\"extract.cgi?id={id}\" style=\"margin-left:20px;width:90px;\" />"
      images += f"<div style=\"font-size:10pt;\">({id}) {title1}</div>"
      images += "</div>\n"
    images += "</div>\n"
    self.setPlaceHolder('content', "")
    self.setPlaceHolder('images', images)
    return

  # 最小の id を得る。
  def getMinId(self) :
    n = self.__mysql.getValue("SELECT MIN(id) FROM BINDATA")
    return n

  # 最大の id を得る。
  def getMaxId(self) :
    n = self.__mysql.getValue("SELECT MAX(id) FROM BINDATA")
    return n

    
# 応答をクライアントへ返す。
wp = BinDataPage('templates/index.html')
wp.echo()
