#!C:\python3\python.exe
# -*- code=utf-8 -*-
# Videos テーブルのワードフィルタ
#   MySQL を利用
from WebPage import WebPage

# CGI WebPage クラス
class MainPage(WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.setPlaceHolder('message', "")

# メイン開始位置
wp = MainPage('templates/filter.html')
wp.echo()
