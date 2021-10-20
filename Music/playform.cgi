#!C:/python3/python.exe
#!/usr/bin/python3

from MySQL import MySQL
from WebPage import WebPage

# CGI WebPage クラス
class MainPage(WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    mysql = MySQL()
    id = self.getParam('id')
    title = mysql.getValue('SELECT title FROM Music WHERE id=' + id)
    self.setPlaceHolder('id', id)
    self.setPlaceHolder('title', title)
    return

# メイン開始位置
wp = MainPage('templates/playform.html')
wp.echo()
