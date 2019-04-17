#!/usr/bin/python3
# -*- code=utf-8 -*-
#   MySQL-IS insert.cgi  Version 2.00
import WebPage as web
import MySQL

# CGI WebPage クラス
class MainPage(web.WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.__mysql = MySQL.MySQL()
    self.schema = self.conf['db']
    self.getTables()
    if self.isParam("submit") :
      self.insert()
    else :
      self.setPlaceHolder('message', '')
    return

  # データ挿入
  def insert(self) :
    table = self.getParam('table')
    fields = self.getParam('fields')
    data = self.getParam('data')
    sql = f"INSERT INTO {table}({fields}) VALUES({data})"
    self.__mysql.execute(sql)
    self.setPlaceHolder('message', 'データが挿入されました。')
    return

  # テーブル一覧を得る。
  def getTables(self) :
    sql = f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE' AND TABLE_SCHEMA='{self.schema}'"
    rows = self.__mysql.query(sql)
    buff = ""
    for row in rows :
      tableName = row[0]
      buff += f"<option>{tableName}</option>"
    self.setPlaceHolder('tables', buff)
    return

# メイン開始位置
wp = MainPage('templates/insert.html')
wp.echo()
