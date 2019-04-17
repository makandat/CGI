#!/usr/bin/env python3
#!C:\Program Files (x86)\Python37\python.exe
#  BINDATA バイナリファイル index.cgi
import WebPage as cgi
import Text as text
import MySQL as mysql
import FileSystem as fs

SELECT = "SELECT id, title, original, datatype, info, size FROM BINDATA"

class BinDataPage(cgi.WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.__mysql = mysql.MySQL()
    if self.isParam('filter') :
      filter = self.getParam('filter')
      if filter == "image" :
        # 画像
        where = " WHERE datatype='.jpg' OR datatype='.png' OR datatype='.gif'"
        self.setPlaceHolder('content', self.getContent(where))
        self.setPlaceHolder('images', self.getImages())
      elif filter == "audio" :
        # 音声
        where = " WHERE datatype='.wav' OR datatype='.mp4' OR datatype='.m4a'"
        self.setPlaceHolder('content', self.getContent(where))
        self.setPlaceHolder('images', "")
      elif filter == "zip" :
        # 圧縮ファイル
        where = " WHERE datatype='.zip' OR datatype='.gz' OR datatype='.bz2'"
        self.setPlaceHolder('content', self.getContent(where))
        self.setPlaceHolder('images', "")
      else :
        self.setPlaceHolder('content', "<tr><td>不正なパラメータ</td></tr>")
        self.setPlaceHolder('images', "")
    else :
      self.setPlaceHolder('content', self.getContent())
      self.setPlaceHolder('images', "")
    return

  # BINDATA テーブルの内容一覧を得る。
  def getContent(self, where="") :
    buff = ""
    rows = self.__mysql.query(SELECT + where)
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
    return buff

  # 画像一覧を得る。
  def getImages(self) :
    images = ""
    rows = self.__mysql.query(SELECT + " WHERE  datatype='.jpg' OR datatype='.png' OR datatype='.gif'")
    for row in rows :
      id = str(row[0])
      title = row[1]
      images += "<li>"
      images += f"<img src=\"extract.cgi?id={id}\" />"
      images += f"<br />{title}"
      images += "</li>\n"
    return images
    
    

# 応答をクライアントへ返す。
wp = BinDataPage('templates/index.html')
wp.echo()
