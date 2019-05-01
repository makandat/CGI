#!/usr/bin/env python3
#!C:\Program Files (x86)\Python37\python.exe
# -*- code=utf-8 -*-
#  Music / index.cgi  Ver.1.10 2019-05-01
from WebPage import WebPage
import FileSystem as fsys
from MySQL import MySQL
import Common

SELECT = 'SELECT id, title, path, artist, album, mark, info, fav, count, bindata, alindex FROM Music'

# CGI WebPage クラス
class MainPage(WebPage) :
  LIMIT = 100
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    #Common.init_logger('/var/www/data/Logger.log')
    try :
      rows = []
      # ページング用クッキーを得る。
      self.pagefid = 0
      if self.isCookie('pagefid') :
        self.pagefid = int(self.getCookie('pagefid'))
      # filter place holder
      self.setPlaceHolder('filter', "")
      # orderby 初期化
      if self.isCookie('orderby') :
        self.orderby = self.getCookie('orderby')
      else :
        self.orderby = "ASC"
        self.setCookie('orderby', self.orderby)
      # MySQL オブジェクトを作成
      self.__mysql = MySQL()
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
      elif self.isParam('id') :
        # id 指定がある場合
        if self.orderby == "ASC" :
          id = '0' if self.getParam('id') == "" else self.getParam('id')
          sql = SELECT + " WHERE id >= " + id + " ORDER BY id " + self.orderby + " LIMIT " + str(MainPage.LIMIT)
        else :
          id = str(self.getMaxId()) if self.getParam('id') == "" else self.getParam('id')
          sql = SELECT + " WHERE id <= " + str(id) + " ORDER BY id " + self.orderby + " LIMIT " + str(MainPage.LIMIT)
        rows = self.__mysql.query(sql)
      else :
        # フィルタ指定がない(通常の)場合
        if self.isParam('reverse') :  # 表示順を確認
          if self.orderby == "ASC" :
            self.orderby = 'DESC'
          else :
            self.orderby = 'ASC'
          self.setCookie('orderby', self.orderby)
        sql = self.paging()
        rows = self.__mysql.query(sql)
      self.setPlaceHolder('result', "")
      # クエリー
      self.setPlaceHolder('result', self.getResult(rows))
      self.setPlaceHolder('message', "クエリー OK")
      if len(rows) == 0 :
        self.setPlaceHolder('message', "０件のデータが検出されました。")
    except Exception as e:
      self.setPlaceHolder('message', "致命的エラーを検出。" + str(e))
      self.setPlaceHolder('result', '')

  # クエリー結果を表にする。
  def getResult(self, rows) :
    result = ""
    for row in rows :
      td = []
      td.append(row[0])
      td.append(row[1])
      td.append(row[2])
      td.append(MainPage.setNoneToEmpty(row[3]))
      td.append(MainPage.setNoneToEmpty(row[4]))
      td.append(MainPage.setNoneToEmpty(row[5]))
      td.append(MainPage.setNoneToEmpty(row[6]))
      td.append(row[7])
      td.append(row[8])
      td.append(row[9])
      td.append(row[10])
      result += WebPage.table_row(td) + "\n"
      self.pagefid = row[0]
    self.setCookie('pagefid', self.pagefid)
    return result

  # SQL を作る。
  def makeFilterSql(self, filter) :
    sql = SELECT + f" WHERE `title` LIKE '%{filter}%' UNION "
    sql += SELECT + f" WHERE `path` LIKE '%{filter}%' UNION "
    sql += SELECT + f" WHERE `album` LIKE '%{filter}%' UNION "
    sql += SELECT + f" WHERE `info` LIKE '%{filter}%'"
    return sql

  # id の最大値を得る。
  def getMaxId(self) :
    maxid = self.__mysql.getValue("SELECT MAX(id) FROM Music")
    return maxid

  # ページング処理 (ページごとのSQLを返す)
  def paging(self) :
    sql = SELECT
    if self.isParam('page') :  # ページ指定
      page = self.getParam('page')
      if page == 'first' :  # 先頭へ
        sql += " ORDER BY id " + self.orderby + " LIMIT " + str(MainPage.LIMIT)
      elif page == 'prev' :  # 前へ
         if self.orderby == "ASC" :
           sql += " WHERE id > " + str(self.pagefid - 2*MainPage.LIMIT) + " ORDER BY id " + self.orderby + " LIMIT " + str(MainPage.LIMIT)
         else :
           sql += " WHERE id < " + str(self.pagefid + 2*MainPage.LIMIT) + " ORDER BY id " + self.orderby + " LIMIT " + str(MainPage.LIMIT)
      elif page == 'next' :  # 次へ
        if self.orderby == "ASC" :
          sql += " WHERE id > " + str(self.pagefid) + " ORDER BY id " + self.orderby + " LIMIT " + str(MainPage.LIMIT)
        else :
          sql += " WHERE id < " + str(self.pagefid) + " ORDER BY id " + self.orderby + " LIMIT " + str(MainPage.LIMIT)
      elif page == 'last' :  # 最後へ
        if self.orderby == "ASC" :
          maxid = self.getMaxId()
          sql += " WHERE id > " + str(maxid - MainPage.LIMIT - 10) + " ORDER BY id " + self.orderby + " LIMIT " + str(MainPage.LIMIT)
        else :
          sql += " WHERE id < " + str(MainPage.LIMIT) + " ORDER BY id " + self.orderby + " LIMIT " + str(MainPage.LIMIT)
      else :
        pass
    else :
      sql += " ORDER BY id " + self.orderby + " LIMIT " + str(MainPage.LIMIT)
    return sql
    
  # 引数が None の場合、"" に変換する。
  @staticmethod
  def setNoneToEmpty(v) :
    if v == None :
      return ""
    else :
      return v

# メイン開始位置
wp = MainPage('templates/index.html')
wp.echo()
