#!/usr/bin/env python3
#  YJFX 資産・取引管理

import WebPage as page
import Text
import MySQL

SELECT_A = 'SELECT id, `date`, FORMAT(asset, 0), FORMAT(profit_loss, 0), FORMAT(asset + profit_loss, 0) AS eval_asset FROM YJFX_Asset'
SELECT_S = 'SELECT id, CurrencyPair, Sell, price1, Date1, price2, Date2, FORMAT(Benefit, 0) FROM YJFX_Settle'
SELECT_SS = 'SELECT FORMAT(SUM(Benefit), 0) AS Profit FROM YJFX_Settle'

# CGI WebPage クラス
class MainPage(page.WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.__mysql = MySQL.MySQL()
    # YJFX_ASSET
    sql = SELECT_A + " ORDER BY id DESC"
    rows = self.__mysql.query(sql)
    self.vars['asset'] = self.getHtml(rows)
    # YJFX_Settle
    if 'span' in self.params :
      span = Text.split('-', self.params['span'].value)
      date_from = '20' + span[0]
      date_to = '20' + span[1]
      sql = SELECT_S + f" WHERE date2 BETWEEN '{date_from}' AND '{date_to}'"
      rows = self.__mysql.query(sql)
      sql = SELECT_SS + f" WHERE date2 BETWEEN '{date_from}' AND '{date_to}'"
      self.vars['sum'] = self.__mysql.getValue(sql)
    else :
      sql = SELECT_S + " ORDER BY id DESC"
      rows = self.__mysql.query(sql)
      self.vars['sum'] = self.__mysql.getValue(SELECT_SS)
    self.vars['settle'] = self.getHtml(rows)
    return

  # クエリー結果をHTMLとして返す。
  def getHtml(self, rows) :
    buff = ""
    for row in rows :
      buff += page.WebPage.table_row(row)
      buff += "\n"
    return buff



# メイン開始位置
wp = MainPage('templates/index.html')
wp.echo()
