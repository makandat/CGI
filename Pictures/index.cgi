#!/usr/bin/env python3
# -*- code=utf-8 -*-
import WebPage as page
import MySQL

SELECT = 'SELECT id, title, creator, path, mark, info, fav, count FROM Pictures'
LIMIT = 500

# CGI WebPage クラス
class MainPage(page.WebPage) :

  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.vars['result'] = ""
    try :
      rows = []
      self.cookie('reverse', '0')
      self.vars['filter'] = ""
      self.vars['reverse'] = 'yes'
      self.__mysql = MySQL.MySQL()
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
      elif 'reverse' in self.params :
        # reverse 指定がある場合
        reverse = self.params['reverse'].value
        if reverse == 'yes' :
          self.vars['reverse'] = 'no'
          self.cookie('reverse', '1')
          sql = SELECT + f" ORDER BY id DESC LIMIT {LIMIT}"
        else :
          self.cookie('reverse', '0')
          self.vars['reverse'] = 'yes'
          sql = SELECT + f" ORDER BY id ASC LIMIT {LIMIT}"
        rows = self.__mysql.query(sql)
      elif 'page' in self.params :
        # page 指定がある場合
        page = self.params['page'].value
        if page == "first" :
          # 先頭のページ
          sql = SELECT + f" LIMIT {LIMIT}"
          rows = self.__mysql.query(sql)
          self.cookie('start_id', str(rows[0][0]))
          n = len(rows) - 1
          self.cookie('end_id', str(rows[n][0]))
        elif page == "prev" :
          # 前のページ
          start = 0
          if 'start_id' in self.cookies :
            start = self.cookies['start_id'].value
          sql = SELECT + f" WHERE id < {start} ORDER BY id DESC LIMIT {LIMIT}"
          rows = self.__mysql.query(sql)
          self.cookie('start_id', str(rows[0][0]))
          n = len(rows) - 1
          self.cookie('end_id', str(rows[n][0]))
        elif page == "next" :
          # 次のページ
          end = 0
          if 'end_id' in self.cookies :
            end = self.cookies['end_id'].value
          sql = SELECT + f" WHERE id > {end} LIMIT {LIMIT}"
          rows = self.__mysql.query(sql)
          self.cookie('start_id', str(rows[0][0]))
          n = len(rows) - 1
          self.cookie('end_id', str(rows[n][0]))
        else : # page == last 
          # 最後のページ
          sql = SELECT + f" ORDER BY id DESC LIMIT {LIMIT}"
          rows = self.__mysql.query(sql)
          self.cookie('start_id', str(rows[0][0]))
          n = len(rows) - 1
          self.cookie('end_id', str(rows[n][0]))
      else :
        # フィルタ指定がない(通常の)場合
        rows = self.__mysql.query(SELECT + f" LIMIT {LIMIT};")
        self.cookie('start_id', str(rows[0][0]))
        n = len(rows) - 1
        self.cookie('end_id', str(rows[n][0]))
        self.vars['result'] = ""
      # クエリー結果を表示する。
      self.vars['result'] = self.getResult(rows)
      self.vars['message'] = "クエリー OK"
      if len(rows) == 0 :
        self.vars['message'] = "０件のデータが検出されました。"
    except Exception as e:
      self.vars['message'] = "致命的エラーを検出。" + str(e)
    return



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




# メイン開始位置
wp = MainPage('templates/index.html')
wp.echo()
