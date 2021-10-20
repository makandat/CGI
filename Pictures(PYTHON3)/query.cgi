#!C:\python3\python.exe
# -*- code=utf-8 -*-
# Pictures テーブルの検索 query.cgi
#   MySQL を利用
from WebPage import WebPage
import FileSystem as fsys
from MySQL import MySQL

# CGI WebPage クラス
class MainPage(WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.__mysql = MySQL()
    self.makeCriteria()
    self.setPlaceHolder('message', '')
    return

  # クエリ条件を作成する。
  def makeCriteria(self) :
    s = ""
    for key, val in self.conf.items() :
      if key.startswith('c') :
        s += "<option>" + val + "</option>\n"
    self.setPlaceHolder('listsql', s)
    return

# メイン開始位置
wp = MainPage('templates/query.html')
wp.echo()
