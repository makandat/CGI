#!/usr/bin/env python3
# -*- code=utf-8 -*-
# MySQL Videos テーブル
import WebPage as page
import FileSystem as fsys
import MySQL

SELECT = 'SELECT id, title, path, creator, series, mark, info, fav, count FROM Videos'

# CGI WebPage クラス
class MainPage(page.WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    try :
      rows = []
      self.__mysql = MySQL.MySQL()
      self.vars['filter'] = ""
      if 'filter' in self.params :
        # フィルタ指定がある場合
        filter = self.params['filter'].value
        self.vars['filter'] = "[設定フィルタ] \"" + filter + '"　<a href="index.cgi">(リセット)</a>'
        sql = self.makeFilterSql(filter)
        rows = self.__mysql.query(sql)
      elif 'fav' in self.params :
        # fav 指定がある場合
        sql = SELECT + " WHERE fav = '1' or fav = '2'"
        rows = self.__mysql.query(sql)
      elif 'mark' in self.params :
        # mark 指定がある場合
        mark = self.params['mark'].value
        sql = SELECT + f" WHERE mark = '{mark}'"
        rows = self.__mysql.query(sql)
      else :
        # フィルタ指定がない(通常の)場合
        rows = self.__mysql.query(SELECT + " LIMIT 1000;")
      self.vars['result'] = ""
      # クエリー
      self.vars['result'] = self.getResult(rows)
      self.vars['message'] = "クエリー OK"
      if len(rows) == 0 :
        self.vars['message'] = "０件のデータが検出されました。"
    except Exception as e:
      self.vars['message'] = "致命的エラーを検出。" + str(e)

  # クエリー結果を表にする。
  def getResult(self, rows) :
    result = ""
    for row in rows :
      result += page.WebPage.table_row(row) + "\n"
    return result

  # SQL を作る。
  def makeFilterSql(self, filter) :
    sql = SELECT + f" WHERE `title` LIKE '%{filter}%' UNION "
    sql += SELECT + f" WHERE `path` LIKE '%{filter}%' UNION "
    sql += SELECT + f" WHERE `series` LIKE '%{filter}%' UNION "
    sql += SELECT + f" WHERE `info` LIKE '%{filter}%'"
    return sql

# メイン開始位置
wp = MainPage('templates/index.html')
wp.echo()
