#!/usr/bin/env python3
# -*- code=utf-8 -*-
# Pictures テーブル フォルダ内画像一覧
#   MySQL を利用
import WebPage as page
import FileSystem as fs
import MySQL
import Common
import Text
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
    files = fs.listFiles(folder)
    for f in files :
      buff += "<figure>"
      buff += f"<img src=\"getImage.cgi?id={id}\" /><figcaption>{f}</figcaption>"
      buff += "</figure>\n"
    return buff

# メイン開始位置
wp = MainPage('templates/listpics.html')
wp.echo()

