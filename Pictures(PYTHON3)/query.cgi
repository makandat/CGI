#!C:\Program Files (x86)\Python37\python.exe
# -*- code=utf-8 -*-
# Pictures テーブルの検索
#   MySQL を利用
import WebPage as page
import FileSystem as fsys
import MySQL

# CGI WebPage クラス
class MainPage(page.WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.__mysql = MySQL.MySQL()
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
