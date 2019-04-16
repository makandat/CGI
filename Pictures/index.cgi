#!/usr/bin/env python3
#!C:\Program Files (x86)\Python37\python.exe
# -*- code=utf-8 -*-
#   index.cgi  Version 3.0
import WebPage as page
import MySQL
import Common
#from syslog import syslog

SELECT = 'SELECT id, title, creator, path, mark, info, fav, count, bindata FROM Pictures'
LIMIT = 500

# CGI WebPage クラス
class MainPage(page.WebPage) :

  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    # Common.init_logger("C:/temp/PyLogger.log")
    self.setPlaceHolder('result', "")
    try :
      rows = []
      self.setPlaceHolder('filter', "")
      self.__mysql = MySQL.MySQL()
      # テーブル情報を表示
      self.setPlaceHolder("tableInfo", self.tableInfo())
      # フィルタ別処理
      if self.isParam('filter') :
        # フィルタ指定がある場合
        filter = self.getParam('filter')
        self.setPlaceHolder('filter', "[設定フィルタ] \"" + filter + '"　<a href="index.cgi">(リセット)</a>')
        sql = self.makeFilterSql(filter)
        rows = self.__mysql.query(sql)
        self.resetOrder()
      elif self.isParam('creator') :
        sql = SELECT + " WHERE creator='" + self.getParam('creator') + "'"
        rows = self.__mysql.query(sql)
        self.resetOrder()
      elif self.isParam('fav') :
        # fav 指定がある場合
        sql = SELECT + " WHERE fav > 0"
        rows = self.__mysql.query(sql)
        self.resetOrder("ASC")
      elif self.isParam('mark') :
        # mark 指定がある場合
        mark = self.getParam('mark')
        sql = SELECT + f" WHERE mark = '{mark}'"
        rows = self.__mysql.query(sql)
        self.resetOrder("ASC")
      elif self.isParam('criteria') :
        # 詳細検索
        criteria = self.getParam('criteria')
        sql = "SELECT * FROM Pictures WHERE " + criteria
        rows = self.__mysql.query(sql)
        self.resetOrder()
      elif self.isParam("btnOrder") :
        # フォームのクエリー
        rows = self.btnOrder()
      else :
        # フィルタ指定がない(通常の)場合
        rows = self.queryNormal()
      # end case
      n = len(rows) - 1
      self.setPlaceHolder('result', "")
      # クエリー結果を表示する。
      self.setPlaceHolder('result', self.getResult(rows))
      self.setPlaceHolder('message', "クエリー OK")
      if len(rows) == 0 :
        self.setPlaceHolder('message', "０件のデータが検出されました。")
    except Exception as e:
      self.setPlaceHolder('message', "致命的エラーを検出。" + str(e))
    return

  # 通常のクエリ(フィルタ指定なし)
  def queryNormal(self) :
    self.setPlaceHolder("start_id", "")
    if self.isCookie('order') :
      self.order = self.getCookie("order")
      rows = self.__mysql.query(SELECT + f" ORDER BY id {self.order} LIMIT {LIMIT};")
      if self.order == "DESC" :
        self.setPlaceHolder("ASCchecked", "")
        self.setPlaceHolder("DESCchecked", "checked")
      else :
        self.setPlaceHolder("ASCchecked", "checked")
        self.setPlaceHolder("DESCchecked", "")
    else:
      rows = self.__mysql.query(SELECT + f" ORDER BY id DESC LIMIT {LIMIT};")
      self.order = "DESC"
      self.setCookie("order", "DESC")
      self.setPlaceHolder("ASCchecked", "")
      self.setPlaceHolder("DESCchecked", "checked")
    return rows

  # フォームのクエリー
  def btnOrder(self) :
    # 並び順を得る。
    self.order = self.getParam("orderby")
    self.setCookie("order", self.order)
    # 降順か昇順かを得る。
    if self.isParam("start_id") :
      self.start_id = int(self.getParam("start_id"))
      self.setPlaceHolder("start_id", self.start_id)
    else :
      if self.order == "ASC" :
        self.start_id = 0
      else :
        self.start_id = 1000000
      self.setPlaceHolder("start_id", "")

    # クエリー実行
    if self.order == "DESC" :
      rows = self.__mysql.query(SELECT + f" WHERE id <= {self.start_id} ORDER BY id {self.order} LIMIT {LIMIT};")
      self.setPlaceHolder("DESCchecked", "checked")
      self.setPlaceHolder("ASCchecked", "")
    else :
      rows = self.__mysql.query(SELECT + f" WHERE id >= {self.start_id} ORDER BY id {self.order} LIMIT {LIMIT};")
      self.setPlaceHolder("DESCchecked", "")
      self.setPlaceHolder("ASCchecked", "checked")
    return rows

  # クエリー結果を表にする。
  def getResult(self, rows) :
    result = ""
    for row in rows :
      id = str(row[0])
      fav = str(row[6])
      row2 = list()
      row2.append(str(id))
      row2.append("<a href='listpics.cgi?id={0}' target='_blank'>{1}</a>".format(id, row[1]))
      row2.append(row[2])
      row2.append(row[3])
      row2.append(row[4])
      row2.append(row[5])
      row2.append(f"<a href=\"like.cgi?id={id}\" target=\"_blank\">{fav}</a>")
      row2.append(row[7])
      if row[8] == None :
        row2.append('')
      else :
        bindata = str(row[8])
        link = f"<img src=\"extract.cgi?id={bindata}\" alt=\"{bindata}\" />"
        row2.append(link)
      result += page.WebPage.table_row(row2) + "\n"
    return result

  # SQL を作る。
  def makeFilterSql(self, filter) :
    sql = SELECT + f" WHERE `title` LIKE '%{filter}%' UNION "
    sql += SELECT + f" WHERE `path` LIKE '%{filter}%' UNION "
    sql += SELECT + f" WHERE `creator` LIKE '%{filter}%' UNION "
    sql += SELECT + f" WHERE `info` LIKE '%{filter}%'"
    return sql

  # テーブル情報を得る。
  def tableInfo(self) :
    n = self.__mysql.getValue("SELECT count(id) FROM Pictures")
    minId = self.__mysql.getValue("SELECT min(id) FROM Pictures")
    maxId = self.__mysql.getValue("SELECT max(id) FROM Pictures")
    return f"Pictures テーブルの行数：{n}, 最小 id {minId}, 最大 id {maxId}"

  #  並び順フォームを初期化
  def resetOrder(self, order="DESC") :
    self.setPlaceHolder('start_id', '')
    if order == "DESC" :
      self.setPlaceHolder('DESCchecked', 'checked')
      self.setPlaceHolder('ASCchecked', '')
      self.setCookie('order', 'DESC')
    else :
      self.setPlaceHolder('DESCchecked', '')
      self.setPlaceHolder('ASCchecked', 'checked')
      self.setCookie('order', 'ASC')
    return


# メイン開始位置
wp = MainPage('templates/index.html')
wp.echo()
