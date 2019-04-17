#!/usr/bin/python3
#!C:\Program Files (x86)\Python37\python.exe
# -*- coding: utf-8 -*-
# slideview.cgi フォルダ内画像のスライド表示
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
    if self.isParam('folder') :
      # Postback のとき
      folder = self.getParam('folder')
      slide = self.getParam('slide')
      self.showPicture(folder, slide)
      parts = folder.split('/')
      n = len(parts) - 1
      self.setPlaceHolder('title', parts[n])
      self.setPlaceHolder('folder', folder)
    else :
      # Postback でない
      self.setPlaceHolder('folder', '')
      self.setPlaceHolder('message', '')
      self.setPlaceHolder('title', 'スライド表示')
      self.setPlaceHolder('filename', '')
    return


  # id から path を得る。
  def getPath(self, id) :
    path = self.__mysql.getValue(f"SELECT `path` FROM Pictures WHERE id={id}")
    return path


  # 画像を表示する。
  def showPicture(self, folder, slide) :
    if self.isCookie('current_image') :
      current = int(self.getCookie('current_image'))
    else :
      current = 0
    files = os.listdir(folder.encode('utf8'))
    n = len(files)
    m = n - 1
    files2 = sorted(files)
    if slide == "first" :
      current = 0
      self.setPlaceHolder('message', "最初の画像です。No.0")
    elif slide == "prev" :
      current = (current - 1) if current > 0 else 0
      if current == 0 :
        self.setPlaceHolder('message', '最初の画像です。No.0')
      else :
        self.setPlaceHolder('message', f"No.{current} / {m}の画像です。")
    elif slide == "next" :
      current = (current + 1) if current < (n - 1) else (n - 1)
      if current == n - 1 :
        self.setPlaceHolder('message', f"最後の画像です。No.{current}")
      else :
        self.setPlaceHolder('message', f"No.{current} / {m} の画像です。")
    elif slide == "last" :
      current = n - 1
      self.setPlaceHolder('message', f"最後の画像です。No.{current}")
    else :
      # CURRENT
      current = int(slide)
      self.setPlaceHolder('message', f"No.{current} / {m} の画像です。")
    filename = files2[current].decode('utf8')
    filePath = folder + "/" + filename
    self.setPlaceHolder('filename', '')
    self.setPlaceHolder('filename', filePath)
    self.setCookie('current_image', str(current))
    #if self.isCookie('image_adjust') :
    #  if self.getCookie('image_adjust') == '1' :
    #    self.setPlaceHolder('picture', f"<img src=\"getImage.cgi?path={filePath}\" style=\"padding:10px;width:100%;\" />")
    #  else :
    #    self.setPlaceHolder('picture', f"<img src=\"getImage.cgi?path={filePath}\" style=\"padding:10px;\" />")
    #else :
    self.setPlaceHolder('picture', f"<img src=\"getImage.cgi?path={filePath}\" style=\"padding:10px;\" />")
    self.setPlaceHolder('path', filePath)
    return

  # 画像ファイルなら True を返す。
  @staticmethod
  def isPicture(path) :
    ext = Text.tolower(fs.getExtension(path))
    return (ext == '.jpg' or ext == '.png' or ext == '.gif')



# メイン開始位置
wp = MainPage('templates/slideview.html')
wp.echo()
