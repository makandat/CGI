#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Pictures テーブル フォルダ内画像一覧
#   MySQL を利用
import WebPage as page
import FileSystem as fs
import MySQL
import Common
import Text
import sys, os
from syslog import syslog

## ページクラス
class MainPage(page.WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.__mysql = MySQL.MySQL()
    if 'id' in self.params :
      id = self.params['id'].value
      folder = self.getPath(id)
      self.vars['folder'] = folder
      self.vars['pictures'] = self.getPictures(folder)
      self.incCount(id)
      self.vars['message'] = ''
    else :
      self.vars['message'] = 'id を指定してください。'
    return

  # id から path を得る。
  def getPath(self, id) :
    path = self.__mysql.getValue(f"SELECT `path` FROM Pictures WHERE id={id}")
    return path

  # 画像ファイル一覧を得る。
  def getPictures(self, folder) :
    buff = ""
    files = os.listdir(folder.encode('utf8'))
    files2 = sorted(files)
    for f in files2 :
      fn = folder + "/" + f.decode('utf8')
      if MainPage.isPicture(fn) :
        buff += "<figure>"
        buff += f"<img src=\"getImage.cgi?path={fn}\" /><figcaption>{fn}</figcaption>"
        buff += "</figure>\n"
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




# メイン開始位置
wp = MainPage('templates/listpics.html')
wp.echo()

