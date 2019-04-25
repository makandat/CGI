#!/usr/bin/python3
# -*- code=utf-8 -*-
#   Filerpy filter.cgi  1.01  2019-04-23
from WebPage import WebPage
import FileSystem as fs
#import Common

# CGI WebPage クラス (表示設定画面)
class MainPage(WebPage) :

  # コンストラクタ
  def __init__(self, template="") :
    super().__init__(template)
    #Common.init_logger('/var/www/data/Logger.log')
    # クッキーがあれば取得する。(なければデフォルト値)
    # 隠しファイル
    if self.isCookie('hiddenfile') :
      self.hiddenfile = self.getCookie('hiddenfile')
    else :
      self.hiddenfile = '0'
    # 表示順
    if self.isCookie('orderby') :
      self.orderby = self.getCookie('orderby')
    else :
      self.orderby = "name"
    # 並び順
    if self.isCookie('reverse') :
      self.reverse = self.getCookie('reverse')
    else :
      self.reverse = "asc"
    # HTML value にクッキーの値を設定する。
    self.setValues()
    return

  # HTML value にクッキーの値を設定する。
  def setValues(self) :
    # 隠しファイル
    if self.hiddenfile == '1' :
      self.setPlaceHolder('hiddenfile', 'checked')
    else :
      self.setPlaceHolder('hiddenfile', '')
    # 表示順
    options = ("name", "size", "time", "id")
    for it in options :
      if it == self.orderby :
        self.setPlaceHolder(it, "selected")
      else :
        self.setPlaceHolder(it, "")
    # 並び順
    if self.reverse == 'asc' :
      self.setPlaceHolder('asc', 'checked')
      self.setPlaceHolder('desc', '')
    else :
      self.setPlaceHolder('asc', '')
      self.setPlaceHolder('desc', 'checked')
    return
    
# メイン開始位置
wp = MainPage('templates/filter.html')
wp.echo()
