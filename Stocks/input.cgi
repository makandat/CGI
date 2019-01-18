#!/usr/bin/env python3
#  証券の管理 (入力)
import WebPage as cgi
import MySQL as mysql
from syslog import syslog

INSERT = "INSERT INTO Stocks(`date`, stock_code, amount, current_price, purchased_price, purchased_date, sec_company, info) VALUES('{0}', '{1}', {2}, {3}, {4}, '{5}', '{6}', '{7}')"

# ページクラス
class StockPage(cgi.WebPage) :
  # コンストラクタ
  def __init__(self, template="") :
    super().__init__(template)
    self.__mysql = mysql.MySQL()
    self.vars['message'] = ""
    if self.isParam('date') and self.isParam('stock_code') and self.isParam('current_price') and self.isParam('amount') :
      self.insert()
      self.vars['message'] = "{0} のデータを追加しました。".format(self.getParam('date'))
    else :
      pass
    return

  # テーブル Stocks にデータを挿入する。
  def insert(self) :
    date = self.getParam('date')
    stock_code = self.getParam('stock_code')
    amount = self.getParam('amount')
    current_price = self.getParam('current_price')
    purchased_price = self.getParam('purchased_price')
    if purchased_price == "" :
      purchased_price = '0'
    purchased_date = self.getParam('purchased_date')
    sec_company = self.getParam('sec_company')
    info = self.getParam('info')
    sql = INSERT.format(date, stock_code, amount, current_price, purchased_price, purchased_date, sec_company, info)
    syslog(sql)
    self.__mysql.execute(sql)
    return

# メイン
wp = StockPage('templates/input.html')
wp.echo()
