#!/usr/bin/env python3
#  証券の管理
import WebPage as cgi
import MySQL as mysql

SELECT = "SELECT * FROM Stocks"

# ページクラス
class StockPage(cgi.WebPage) :
  # コンストラクタ
  def __init__(self, template="") :
    super().__init__(template)
    self.__mysql = mysql.MySQL()
    self.vars['message'] = ""
    self.vars['content'] = self.getContent()
    return

  # テーブル Stocks の内容を取得する。
  def getContent(self) :
    sql = SELECT + " ORDER BY `date` DESC"
    rows = self.__mysql.query(sql)
    buff = ""
    for row in rows :
      buff += cgi.WebPage.table_row(row)
    return buff

# メイン
wp = StockPage('templates/index.html')
wp.echo()
