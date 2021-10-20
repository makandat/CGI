#!C:\python3\python.exe
#!/usr/bin/python3
# -*- coding: utf-8 -*-
# フォルダ内画像のサムネール一覧
#   MySQL を利用
import WebPage as page
import FileSystem as fs
import MySQL
import Text
import sys, os
#from syslog import syslog

## ページクラス
class MainPage(page.WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.__mysql = MySQL.MySQL()
    self.setPlaceHolder('title', 'フォルダ内画像のサムネール一覧')
    if self.isParam('id') :
      id = self.getParam('id')
      self.setPlaceHolder('id', id)
      folder = self.getPath(id)
      parts = folder.split('/')
      n = len(parts) - 1
      name = parts[n] if n >= 0 else ''
      self.setPlaceHolder('title', name + "<br /><span style='font-size:0.5em;color:blue;'>フォルダ内画像のサムネール一覧</span>")
      self.setPlaceHolder('title1', name)
      self.setPlaceHolder('folder', folder);
      self.setPlaceHolder('message', '')
      self.setPlaceHolder('pictures', self.getPictures(folder))
    else :
      self.setPlaceHolder('id', '')
      self.setPlaceHolder('folder', '')
      self.setPlaceHolder('pictures', '')
      self.setPlaceHolder('message', 'エラー： フォルダの id が指定されていない。')
      self.setPlaceHolder('title1', 'フォルダ内画像のサムネール一覧')

  # id から path を得る。
  def getPath(self, id) :
    path = self.__mysql.getValue(f"SELECT `path` FROM Pictures WHERE id={id}")
    return path

  # 画像ファイル一覧を得る。
  def getPictures(self, folder) :
    buff = ""
    files = os.listdir(folder.encode('utf8'))
    files2 = sorted(files)
    i = 0
    for f in files2 :
      fn = folder + "/" + f.decode('utf8')
      if MainPage.isPicture(fn) :
        buff += f"<a href=\"slideview.cgi?folder={folder}&slide={i}\" target=\"_blank\"><img src=\"getImage.cgi?path={fn}\" style='width:15%;padding:10px;' /></a>"
        i += 1
      else :
        pass
    return buff

  # 画像ファイルなら True を返す。
  @staticmethod
  def isPicture(path) :
    ext = Text.tolower(fs.getExtension(path))
    return (ext == '.jpg' or ext == '.png' or ext == '.gif')



# メイン開始位置
wp = MainPage('templates/thumbview.html')
wp.echo()
