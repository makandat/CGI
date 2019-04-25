#!/usr/bin/python3
# -*- code=utf-8 -*-
#   MySQL-IS delete.cgi  Version 2.00
import WebPage as web
import MySQL
#from syslog import syslog

# CGI WebPage クラス
class MainPage(web.WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.__mysql = MySQL.MySQL()
    self.schema = self.conf['db']
    self.getTables()
    if self.isParam('submit') :
      self.delete()
    else :
      self.setPlaceHolder('message', "")
    return

  # データを削除する。
  def delete(self) :
    table = self.getParam('table')
    criteria = self.getParam('criteria')
    if criteria == "" :
      self.setPlaceHolder('message', '削除条件が空欄です。')
    else :
      sql = f"DELETE FROM {table} WHERE {criteria}"
      self.__mysql.execute(sql)
      self.setPlaceHolder('message', 'データを削除しました。')     
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
wp = MainPage('templates/delete.html')
wp.echo()
