#!/usr/bin/env python3
#  show_unregitems.cgi 未登録画像一覧
from WebPage import WebPage
from MySQL import MySQL

class UnregItems(WebPage) :
  # コンストラクタ
  def __init__(self, template="") :
    super().__init__(template)
    self.__mysql = MySQL()
    self.showItems()
    return

  # 画像一覧を作成
  def showItems(self) :
    sql = "SELECT * FROM PictureAlbum WHERE album = 0"
    rows = self.__mysql.query(sql)
    if len(rows) == 0 :
      self.setPlaceHolder('content', "<p style=\"text-align:center;padding:10px;color:magenta;font-size:16pt;\">未登録画像はありません。</p>")
      return
    content = ""
    for row in rows :
      content += WebPage.table_row(row)
      content += "\n"
    self.setPlaceHolder('content', content)
    return
    
    
# 開始
wp = UnregItems('templates/show_unregitems.html')
wp.echo()
