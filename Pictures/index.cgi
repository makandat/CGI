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
      self.setPlaceHolder('filter', "")
      self.setPlaceHolder('reverse', 'yes')
      self.__mysql = MySQL.MySQL()
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
      elif self.isParam('criteria') :
        # 詳細検索
        criteria = self.getParam('criteria')
        sql = "SELECT * FROM Pictures WHERE " + criteria
        rows = self.__mysql.query(sql)
      elif self.isParam('reverse') :
        # reverse 指定がある場合
        reverse = self.getParam('reverse')
        if reverse == 'yes' :
          self.setPlaceHolder('reverse', 'no')
          self.cookie('reverse', '1')
          sql = SELECT + f" ORDER BY id DESC LIMIT {LIMIT}"
        else :
          self.cookie('reverse', '0')
          self.setPlaceHolder('reverse', 'yes')
          sql = SELECT + f" ORDER BY id ASC LIMIT {LIMIT}"
        rows = self.__mysql.query(sql)
      elif self.isParam('page') :
        # page 指定がある場合
        page = self.getParam('page')
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
            start = self.getCookie('start_id')
          sql = SELECT + f" WHERE id < {start} ORDER BY id DESC LIMIT {LIMIT}"
          rows = self.__mysql.query(sql)
          self.cookie('start_id', str(rows[0][0]))
          n = len(rows) - 1
          self.cookie('end_id', str(rows[n][0]))
        elif page == "next" :
          # 次のページ
          end = 0
          if 'end_id' in self.cookies :
            end = self.getCookie('end_id')
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
        self.setPlaceHolder('result', "")
      # クエリー結果を表示する。
      self.setPlaceHolder('result', self.getResult(rows))
      self.setPlaceHolder('message', "クエリー OK")
      if len(rows) == 0 :
        self.setPlaceHolder('message', "０件のデータが検出されました。")
    except Exception as e:
      self.setPlaceHolder('message', "致命的エラーを検出。" + str(e))
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
