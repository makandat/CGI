#!/usr/bin/env python3
#  証券の管理 (修正)
import WebPage as cgi
import MySQL as mysql
from syslog import syslog

UPDATE = "UPDATE Stocks SET `date`='{1}', stock_code='{2}', current_price={3}, amount={4}, purchased_price={5}, purchased_date='{6}', sec_company='{7}', info='{8}' WHERE id={0}"
SELECT = "SELECT * FROM Stocks WHERE id={0}"

# ページクラス
class StockPage(cgi.WebPage) :
  # コンストラクタ
  def __init__(self, template="") :
    super().__init__(template)
    self.__mysql = mysql.MySQL()
    self.vars['message'] = ""
    if self.isParam('btnSave') :
      self.modify()
      id = self.getParam('id')
      self.vars['message'] = f"id {id} のデータを更新しました。"
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
      self.vars['message'] = "エラー：不正な id"
      self.clearData()
      return
    row = rows[0]
    self.vars['id'] = id
    self.vars['date'] = row[1]
    self.vars['stock_code'] = row[2]
    self.vars['current_price'] = row[3]
    self.vars['amount'] = row[4]
    self.vars['purchased_price'] = '0' if row[5] == None else row[5]
    self.vars['purchased_date'] = '' if row[6] == None else row[6]
    self.vars['sec_company'] = '' if row[7] == None else row[7]
    self.vars['info'] = '' if row[8] == None else row[8]
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
    self.vars['id'] = ""
    self.vars['date'] = ""
    self.vars['stock_code'] = ""
    self.vars['current_price'] = ""
    self.vars['amount'] = ""
    self.vars['purchased_price'] = ""
    self.vars['purchased_date'] = ""
    self.vars['sec_company'] = ""
    self.vars['info'] = ""
    return

# メイン
wp = StockPage('templates/modify.html')
wp.echo()
