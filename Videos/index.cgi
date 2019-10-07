#!/usr/bin/env python3
#!C:\Program Files (x86)\Python37\python.exe
# -*- code=utf-8 -*-
# MySQL Videos テーブル  ver1.60 2019-10-08  folder フィールド追加対応
from WebPage import WebPage
import Common
from MySQL import MySQL
import math

SELECT = 'SELECT id, title, path, creator, series, mark, info, fav, count, bindata, album, folder FROM Videos'
LIMIT = 100

# CGI WebPage クラス
class MainPage(WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    #Common.init_logger("/home/user/log/Videos.log")
    try :
      rows = []
      self.__mysql = MySQL()
      self.setPlaceHolder('filter', "")
      self.setPlaceHolder('page', "")
      if self.isParam('filter') :
        # フィルタ指定がある場合
        filter = self.getParam('filter')
        self.setPlaceHolder('filter', "[設定フィルタ] \"" + filter + '"　<a href="index.cgi">(リセット)</a>')
        sql = self.makeFilterSql(filter)
        rows = self.__mysql.query(sql)
      elif self.isParam('fav') :
        # fav 指定がある場合
        sql = SELECT + " WHERE fav = '1' or fav = '2'"
        rows = self.__mysql.query(sql)
      elif self.isParam('mark') :
        # mark 指定がある場合
        mark = self.getParam('mark')
        sql = SELECT + f" WHERE mark = '{mark}'"
        rows = self.__mysql.query(sql)
      elif self.isParam('folder') :
        onlyfolder = self.getParam('folder')
        if onlyfolder == "0" :
          sql = SELECT
        else :
          sql = SELECT + f" WHERE folder = '1'"
        rows = self.__mysql.query(sql)
      else :
        # フィルタ指定がない(通常の)場合
        if self.isParam('page') :
          if not self.isCookie('page') :
            self.page = 0
          else :
            self.page = int(self.getCookie('page'))
          nPage = math.floor(self.__mysql.getValue("SELECT count(id) FROM Videos") / LIMIT) + 1
          if self.getParam('page') == 'first' :
            self.page = 0
          elif self.getParam('page') == 'prev' :
            if self.page > 0 :
              self.page -= 1
          elif self.getParam('page') == 'next' :
            if self.page < nPage - 1 :
              self.page += 1
          elif self.getParam('page') == 'last' :
            self.page = nPage - 1
          else :
            pass
          self.setCookie('page', self.page)
          self.setPlaceHolder('page', str(self.page+1) + "/" + str(nPage))
          ids = self.__mysql.query("SELECT id FROM Videos ORDER BY id")
          id0 = ids[self.page * LIMIT][0]
          sql = SELECT + " WHERE id >= {0} ORDER BY id LIMIT {1}".format(id0, LIMIT)
          rows = self.__mysql.query(sql)
        else :
          sql = SELECT + " ORDER BY id LIMIT {0}".format(LIMIT)
          rows = self.__mysql.query(sql)
          self.setCookie('page', '0')
          self.setPlaceHolder('result', "")
      # クエリー
      self.setPlaceHolder('result', self.getResult(rows))
      self.setPlaceHolder('message', "クエリー OK")
      if len(rows) == 0 :
        self.setPlaceHolder('message', "０件のデータが検出されました。")
    except Exception as e:
      self.setPlaceHolder('message', "致命的エラーを検出。" + str(e))
      self.embed({'filter':'', 'result':''})

  # クエリー結果を表にする。
  def getResult(self, rows) :
    result = ""
    for row in rows :
      tr = []
      tr.append(row[0])
      tr.append(row[1])
      tr.append(row[2])
      tr.append(MainPage.NoneToSpace(row[3]))
      tr.append(MainPage.NoneToSpace(row[4]))
      tr.append(MainPage.NoneToSpace(row[5]))
      tr.append(MainPage.NoneToSpace(row[6]))
      tr.append(row[7])
      tr.append(row[8])
      bindata = row[9];
      if bindata == 0 :
        row9 = "0"
      else :
        row9 = f"<img src=\"extract.cgi?id={bindata}\" alt=\"{bindata}\" />"
      tr.append(row9)
      tr.append(row[10])
      tr.append(row[11])
      result += WebPage.table_row(tr) + "\n"
    return result

  # SQL を作る。
  def makeFilterSql(self, filter) :
    sql = SELECT + f" WHERE `title` LIKE '%{filter}%' UNION "
    sql += SELECT + f" WHERE `path` LIKE '%{filter}%' UNION "
    sql += SELECT + f" WHERE `series` LIKE '%{filter}%' UNION "
    sql += SELECT + f" WHERE `info` LIKE '%{filter}%'"
    return sql

  # パラメータが None なら空文字列にする。
  @staticmethod
  def NoneToSpace(s) :
    if s == None :
      return ""
    else :
      return s

# メイン開始位置
wp = MainPage('templates/index.html')
wp.echo()
