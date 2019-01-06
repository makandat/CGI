#!/usr/bin/env python3
# -*- code=utf-8 -*-
import WebPage as page
import MySQL

SELECT = 'SELECT id, title, creator, path, mark, info, fav, count FROM Pictures'
LIMIT = 100

# CGI WebPage クラス
class MainPage(page.WebPage) :

  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    try :
      rows = []
      self.vars['filter'] = ""
      self.vars['reverse'] = 'yes'
      self.__mysql = MySQL.MySQL()
      if 'filter' in self.params :
        # フィルタ指定がある場合
        filter = self.params['filter'].value
        self.vars['filter'] = "[設定フィルタ] \"" + filter + '"　<a href="index.cgi">(リセット)</a>'
        self.vars["start"] = self.getStartId()
        self.vars["end"] = self.getEndId()
        sql = self.makeFilterSql(filter)
        rows = self.__mysql.query(sql)
      elif 'fav' in self.params :
        # fav 指定がある場合
        sql = SELECT + " WHERE fav = '1' or fav = '2'"
        self.vars["start"] = self.getStartId()
        self.vars["end"] = self.getEndId()
        rows = self.__mysql.query(sql)
      elif 'mark' in self.params :
        # mark 指定がある場合
        mark = self.params['mark'].value
        sql = SELECT + f" WHERE mark = '{mark}'"
        self.vars["start"] = self.getStartId()
        self.vars["end"] = self.getEndId()
        rows = self.__mysql.query(sql)
      elif 'reverse' in self.params :
        # reverse 指定がある場合
        reverse = self.params['reverse'].value
        if reverse == 'yes' :
          self.vars['reverse'] = 'no'
          sql = SELECT + f" ORDER BY id DESC LIMIT {LIMIT}"
        else :
          self.vars['reverse'] = 'yes'
          sql = SELECT + f" ORDER BY id ASC LIMIT {LIMIT}"
        rows = self.__mysql.query(sql)
      elif 'idstart' in self.params :
        # idstart 指定がある場合
        start = self.params['idstart'].value
        self.vars["start"] = self.getStartId(start)
        self.vars["end"] = start
        sql = SELECT + f" WHERE id > {start} LIMIT {LIMIT}"
        rows = self.__mysql.query(sql)
      elif 'idend' in self.params :
        # idend 指定がある場合
        end = self.params['idend'].value
        self.vars["start"] = end
        self.vars["end"] = self.getEndId(end)
        sql = SELECT + f" WHERE id BETWEEN {start} AND {end} LIMIT {LIMIT}"
        rows = self.__mysql.query(sql)
      else :
        # フィルタ指定がない(通常の)場合
        rows = self.__mysql.query(SELECT + f" LIMIT {LIMIT};")
        self.vars["start"] = self.getStartId()
        self.vars["end"] = self.getEndId()
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
      row2 = list()
      row2.append(row[0])
      row2.append("<a href='listpics.cgi?id={0}' target='_blank'>{1}</a>".format(row[0], row[1]))
      row2.append(row[2])
      row2.append(row[3])
      row2.append(row[4])
      row2.append(row[5])
      row2.append(row[6])
      row2.append(row[7])
      result += page.WebPage.table_row(row2) + "\n"
    return result

  # SQL を作る。
  def makeFilterSql(self, filter) :
    sql = SELECT + f" WHERE `title` LIKE '%{filter}%' UNION "
    sql += SELECT + f" WHERE `path` LIKE '%{filter}%' UNION "
    sql += SELECT + f" WHERE `creator` LIKE '%{filter}%' UNION "
    sql += SELECT + f" WHERE `info` LIKE '%{filter}%'"
    return sql

  # 先頭の id を得る。
  def getStartId(self, endid=0) :
    if endid == 0 :
      startid = self.__mysql.getValue(f"SELECT MIN(id) FROM Pictures")
    else :
      startid = self.__mysql.getValue(f"SELECT MIN(id) FROM Pictures WHERE id <= {endid} LIMIT {LIMIT}")
    return startid

  # 最終の id を得る。
  def getEndId(self, startid=0) :
    if startid == 0 :
      endid = self.__mysql.getValue(f"SELECT MAX(id) FROM Pictures LIMIT {LIMIT}")
    else :
      endid = self.__mysql.getValue(f"SELECT MAX(id) FROM Pictures WHERE id >= {startid} LIMIT {LIMIT}")
    return endid

# メイン開始位置
wp = MainPage('templates/index.html')
wp.echo()
