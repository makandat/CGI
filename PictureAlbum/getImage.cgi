#!/usr/bin/python3
#!C:\Program Files (x86)\Python37\python.exe
#  画像を返す。
import WebPage as page

class Page(page.WebPage) :
  # コンストラクタ
  def __init__(self) :
    super().__init__(self)
    if 'path' in self.params :
      path = self.getParam('path').encode('utf8')
      Page.sendImage(path)
    else :
      Page.sendImage('/var/www/html/img/error.png')

Page()
