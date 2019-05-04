#!/usr/bin/env python3
#!C:\Program Files (x86)\Python37\python.exe
#  YJFX 資産・取引管理 index.cgi  2019-05-03
from WebPage import WebPage
from MySQL import MySQL
import Text

SELECT_S = 'SELECT id, CurrencyPair, Sell, price1, Date1, price2, Date2, FORMAT(Benefit, 0) FROM YJFX_Settle'
SELECT_SS = 'SELECT FORMAT(SUM(Benefit), 0) AS Profit FROM YJFX_Settle'

# CGI WebPage クラス
class MainPage(WebPage) :
  LIMIT = 1000
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.__mysql = MySQL()
    # 期間の初日と最終日を表示
    self.showSpan()
    # YJFX_Settle
    if self.isParam('span') :
      span = Text.split('-', self.getParam('span'))
      date_from = '20' + span[0]
      date_to = '20' + span[1]
      sql = SELECT_S + f" WHERE date2 BETWEEN '{date_from}' AND '{date_to}' LIMIT {MainPage.LIMIT}"
      rows = self.__mysql.query(sql)
      sql = SELECT_SS + f" WHERE date2 BETWEEN '{date_from}' AND '{date_to}' LIMIT {MainPage.LIMIT}"
      sm = self.__mysql.getValue(sql)
      if sm == None :
        self.setPlaceHolder('sum', 'データがありません。')
      else :
        self.setPlaceHolder('sum', sm)
    else :
      sql = SELECT_S + f" ORDER BY id DESC LIMIT {MainPage.LIMIT}"
      rows = self.__mysql.query(sql)
      self.setPlaceHolder('sum', self.__mysql.getValue(SELECT_SS))
    self.setPlaceHolder('settle', self.getHtml(rows))
    return

  # クエリー結果をHTMLとして返す。
  def getHtml(self, rows) :
    buff = ""
    for row in rows :
      buff += WebPage.table_row(row)
      buff += "\n"
    return buff

  # 期間の初日と最終日を表示
  def showSpan(self) :
    rows = self.__mysql.query("SELECT MIN(Date2), MAX(Date2) FROM YJFX_Settle")
    if len(rows) == 0 :
      self.setPlaceHolder('message', 'データがありません。')
    else :
      row = rows[0]
      self.setPlaceHolder('message', "期間(決済)は {0} から {1} です。".format(row[0], row[1]))
    return



# メイン開始位置
wp = MainPage('templates/index2.html')
wp.echo()
