#!/usr/bin/env python3
#!C:\Program Files (x86)\Python37\python.exe
#  証券の管理 (修正)
from WebPage import WebPage
from MySQL import MySQL
#from syslog import syslog

UPDATE = "UPDATE Stocks SET `date`='{1}', stock_code='{2}', current_price={3}, amount={4}, purchased_price={5}, purchased_date='{6}', sec_company='{7}', info='{8}' WHERE id={0}"
SELECT = "SELECT * FROM Stocks WHERE id={0}"

# ページクラス
class StockPage(WebPage) :
  # コンストラクタ
  def __init__(self, template="") :
    super().__init__(template)
    self.__mysql = MySQL()
    self.setPlaceHolder('message', "")
    if self.isParam('btnSave') :
      self.modify()
      id = self.getParam('id')
      self.setPlaceHolder('message', f"id {id} のデータを更新しました。")
      self.clearData()
    elif self.isParam('btnQuery') and self.isParam('id') :
      id = self.getParam('id')
      self.getContent(id)
    else :
      self.clearData()
    return

  # テーブル Stocks の内容を取得する。
  def getContent(self, id) :
    sql = SELECT.format(id)
    rows = self.__mysql.query(sql)
    if len(rows) == 0 :
      self.setPlaceHolder('message', "エラー：不正な id")
      self.clearData()
      return
    row = rows[0]
    purchased_price = '0' if row[5] == None else row[5]
    purchased_date = '' if row[6] == None else row[6]
    sec_company = '' if row[7] == None else row[7]
    info = '' if row[8] == None else row[8]
    self.embed({'id':id, 'date':row[1], 'stock_code':row[2], 'current_price':row[3], 'amount':row[4], 'purchased_price':purchased_price, 'purchased_date':purchased_date, 'sec_company':sec_company, 'info':info})
    return
      
  # テーブル Stocks の内容を更新する。
  def modify(self) :
    id = self.getParam('id')
    date = self.getParam('date')
    stock_code = self.getParam('stock_code')
    current_price = self.getParam('current_price')
    amount = self.getParam('amount')
    purchased_price = '0' if self.getParam('purchased_price') == '' else self.getParam('purchased_price')
    purchased_date = self.getParam('purchased_date')
    sec_company = self.getParam('sec_company')
    info = self.getParam('info')
    sql = UPDATE.format(id, date, stock_code, current_price, amount, purchased_price, purchased_date, sec_company, info)
    syslog(sql)
    self.__mysql.execute(sql)
    return

  # 表示をクリアする。
  def clearData(self) :
    self.embed({'id':'', 'date':'', 'stock_code':'', 'current_price':'', 'amount':'', 'purchased_price':'', 'purchased_date':'', 'sec_company':'', 'info':''})
    return

# メイン
wp = StockPage('templates/modify.html')
wp.echo()
