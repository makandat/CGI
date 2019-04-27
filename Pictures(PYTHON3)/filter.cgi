#!/usr/bin/python3
#!C:\Program Files (x86)\Python37\python.exe
# -*- code=utf-8 -*-
# Videos テーブルのワードフィルタ
#   MySQL を利用
import WebPage as page
import FileSystem as fsys
import MySQL

# CGI WebPage クラス
class MainPage(page.WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.setPlaceHolder('message', "")

# メイン開始位置
wp = MainPage('templates/filter.html')
wp.echo()
