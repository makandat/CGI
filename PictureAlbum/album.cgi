#!/usr/bin/env python3
#!C:\Program Files (x86)\Python37\python.exe
# -*- code=utf-8 -*-
#   album.cgi  Version 1.00
from WebPage import WebPage
from MySQL import MySQL
import FileSystem as fs
import Common
#from syslog import syslog

LIMIT = 200

# CGI WebPage クラス
class MainPage(WebPage) :

  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    return

# 実行開始
wp = MainPage('templates/album.html')
wp.echo()
