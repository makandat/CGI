#!/usr/bin/python3
#!C:\Program Files (x86)\Python37\python.exe
# -*- coding: utf-8 -*-
# Pictures テーブル フォルダ内画像一覧  Version 3.73  2019-10-27
#   MySQL を利用
from WebPage import WebPage
import FileSystem as fs
from MySQL import MySQL
import Common
import Text
import sys, os
#from syslog import syslog

## ページクラス
class MainPage(WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.__mysql = MySQL()
    if self.isParam('id') :
      id = self.getParam('id')
      folder = self.getPath(id)
      self.setPlaceHolder('id', id)
      self.setPlaceHolder('folder', folder)
      self.setPlaceHolder('creator', self.getCreator(id));
      self.setPlaceHolder('title', self.getTitle(id));
      reverse = False
      if self.isParam("reverse") :
        reverse = True if self.getParam("reverse") == "1" else False
      self.setPlaceHolder('pictures', self.getPictures(folder, reverse))
      self.incCount(id)
      self.setPlaceHolder('id', id)
      if self.getPlaceHolder('message') == "" :
        self.setPlaceHolder('message', '画像をクリックすると画像のパス名リストに追加され、「パス一覧を表示」により表示できます。。')
    else :
      self.setPlaceHolder('message', 'id を指定してください。')
      self.setPlaceHolder('id', '')
      self.setPlaceHolder('creator', 'unknown');
    return

  # id から path を得る。
  def getPath(self, id) :
    path = self.__mysql.getValue(f"SELECT `path` FROM Pictures WHERE id={id}")
    return path

  # 画像ファイル一覧を得る。
  def getPictures(self, folder, reverse=False) :
    buff = ""
    files = os.listdir(folder.encode('utf8'))
    if len(files) == 0 :
      self.setPlaceHolder('message', 'このフォルダにはファイルがありません。')
    else :
      self.setPlaceHolder('message', '')
    files2 = sorted(files, reverse=reverse)
    i = 1
    for f in files2 :
      fn = folder + "/" + f.decode('utf8')
      size = fs.getFileSize(fn) 
      udate = fs.getLastWrite(fn) 
      if MainPage.isPicture(fn) :
        buff += "<figure>"
        buff += "<img src=\"getImage.cgi?path={1}\" /><figcaption><span style='color:black;font-weight:bold;'>{0:04d} {1} </span><span style='color:gray;'>(updated:{2}, size:{3})</span></figcaption>".format(i, fn, udate, size)
        buff += "</figure>\n"
        i += 1
      else :
        pass
    return buff

  # COUNT を増加させる。
  def incCount(self, id) :
    n = self.__mysql.getValue(f"SELECT count FROM Pictures WHERE id={id}")
    n += 1
    self.__mysql.execute(f"UPDATE Pictures SET count={n} WHERE id={id}")
    return

  # 画像ファイルなら True を返す。
  @staticmethod
  def isPicture(path) :
    ext = Text.tolower(fs.getExtension(path))
    return (ext == '.jpg' or ext == '.png' or ext == '.gif')

  # 作者を得る。
  def getCreator(self, id) :
    creator = self.__mysql.getValue(f"SELECT creator FROM Pictures WHERE id={id}") 
    return creator
    
  # タイトルを得る。
  def getTitle(self, id) :
    title = self.__mysql.getValue(f"SELECT title FROM Pictures WHERE id={id}") 
    return title



# メイン開始位置
wp = MainPage('templates/listpics.html')
wp.echo()

