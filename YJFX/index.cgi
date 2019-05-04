#!/usr/bin/env python3
#!C:\Program Files (x86)\Python37\python.exe
#  YJFX 資産・取引管理 index.cgi  2019-05-03
from WebPage import WebPage
from MySQL import MySQL
import Text
import Common

SELECT_A = 'SELECT id, `date`, FORMAT(asset, 0), FORMAT(profit_loss, 0), FORMAT(asset + profit_loss, 0) AS eval_asset FROM YJFX_Asset'

# CGI WebPage クラス
class MainPage(WebPage) :
  LIMIT = 100
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    #Common.init_logger('c:/temp/Logger.log')
    self.__mysql = MySQL()
    self.showInfo()
    # ポストバックかどうか？
    if self.isParam('id') :
     id = self.getParam('id')
     self.pageView(id)
    else :
      sql = SELECT_A + " ORDER BY id DESC LIMIT " + str(MainPage.LIMIT)
      rows = self.__mysql.query(sql)
      self.setPlaceHolder('asset', self.getHtml(rows))
    return


  # ページを表示する。
  def pageView(self, id) :
    sql = SELECT_A
    if id == 'last' :
      # 最後
      sql += " ORDER BY id DESC LIMIT " + str(MainPage.LIMIT)
    elif id == 'prev' :
      # 前へ (逆順表示なのでidが大きい方へ)
      idf = 1000000
      if self.isCookie('idf') :
        idf = int(self.getCookie('idf'))
      sql += " WHERE id < {0} ORDER BY id DESC LIMIT {1}".format(idf + MainPage.LIMIT, MainPage.LIMIT)
    elif id == 'next' :
      # 次へ (逆順表示なのでidが小さい方へ)
      idl = 100000
      if self.isCookie('idl') :
        idl = self.getCookie('idl')
        sql += " WHERE id < {0} ORDER BY id DESC LIMIT {1}".format(idl,  MainPage.LIMIT)
    elif id == 'first' :
      # 最初
      min = self.getMinId()
      sql += " WHERE id < {0} ORDER BY id DESC LIMIT {1}".format(min + MainPage.LIMIT, MainPage.LIMIT)
    else :
      if id == "" :
        id = 1000000
      else :
        id = int(id)
      sql += " WHERE id <= {0} ORDER BY id DESC LIMIT {1}".format(id, MainPage.LIMIT)
    rows = self.__mysql.query(sql)
    self.setPlaceHolder('asset', self.getHtml(rows))
    return

  # クエリー結果をHTMLとして返す。
  def getHtml(self, rows) :
    buff = ""
    idf = 0   # 最初の id (id が大きい)
    idl = 0   # 最後の id (id が小さい)
    for row in rows :
      if idf == 0 :
        idf = row[0]
      idl = row[0]
      buff += WebPage.table_row(row)
      buff += "\n"
    # クッキーに idr, idn を保存する。
    self.setCookie('idf', idf)
    self.setCookie('idl', idl)
    return buff

  # 最小の id を得る。
  def getMinId(self) :
    min = self.__mysql.getValue('SELECT MIN(id) FROM YJFX_Asset')
    return min

  # テーブルの状況を表示する。
  def showInfo(self) :
    rows = self.__mysql.query("SELECT count(id), max(id), min(id) FROM YJFX_Asset")
    if len(rows) == 0 :
      self.setPlaceHolder('message', 'YJFX_Asset テーブルのデータがありません。')
    else :
      row = rows[0]
      msg = "YJFX_Asset テーブルの行数 = {0}, 番号(id)の最大値 = {1}, 番号(id)の最小値 = {2}".format(row[0], row[1], row[2])
      self.setPlaceHolder('message', msg)
    return

# メイン開始位置
wp = MainPage('templates/index.html')
wp.echo()
