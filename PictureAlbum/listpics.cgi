#!/usr/bin/python3
#!C:\Program Files (x86)\Python37\python.exe
# -*- coding: utf-8 -*-
# Pictures テーブル フォルダ内画像一覧  v1.20
#   MySQL を利用
from WebPage import WebPage
import FileSystem as fs
import MySQL
import Common
import Text
import sys, os
#from syslog import syslog

## ページクラス
class MainPage(WebPage) :
  # コンストラクタ
  def __init__(self, template="") :
    super().__init__(template)
    self.__mysql = MySQL.MySQL()
    if self.isParam('id') :
      album = self.getParam('id')
      albumName = self.getAlbumName(album)
      self.setPlaceHolder('title', f"アルバム#{album} {albumName}")
      self.setPlaceHolder('message', '')
      self.getPictures(album)
    else :
      self.setPlaceHolder('message', 'アルバム番号 (id) を指定してください。')
      self.setPlaceHolder('pictures', '');
    return

  # アルバム番号から名称を得る。
  def getAlbumName(self, id) :
    sql = f"SELECT name FROM Album WHERE id={id}"
    name = self.__mysql.getValue(sql)
    return name

  # 画像ファイル一覧を得る。
  def getPictures(self, album) :
    buff = ""
    sql = f"SELECT title, path, picturesid FROM PictureAlbum WHERE album={album}"
    rows = self.__mysql.query(sql)
    if len(rows) == 0 :
      self.setPlaceHolder('message', 'このアルバムには画像がありません。')
      self.setPlaceHolder('pictures', '')
      return
    i = 1
    for row in rows :
      path = row[1]
      title = row[0]
      picturesid = row[2]
      if picturesid == None or picturesid == 0 :
        buff += f"<a href=\"slideview.cgi?album={album}&slide={i}\" target=\"_blank\"><img src=\"getImage.cgi?path={path}\" alt=\"{title}\" style=\"width:20%;padding:6px;\" /></a>"
      else :
        buff += f"<a href=\"/cgi-bin/Pictures/thumbview.cgi?id={picturesid}\" target=\"_blank\"><img src=\"getImage.cgi?path={path}\" alt=\"{title}\" style=\"width:20%;padding:6px;border:solid 2px blue;\" /></a>"
      i += 1
    self.setPlaceHolder('pictures', buff)
    return



# メイン開始位置
wp = MainPage('templates/listpics.html')
wp.echo()

