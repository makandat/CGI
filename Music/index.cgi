#!C:\python3\python.exe
#!/usr/bin/env python3
# -*- code=utf-8 -*-
#  index.cgi
from WebPage import WebPage
import FileSystem as fsys
from MySQL import MySQL

SELECT = "SELECT id, album, title, `path`, artist, album, mark, info, fav, count, bindata, date_format(`date`, '%Y-%m-%d') as `date` FROM Music"

# CGI WebPage クラス
class MainPage(WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    try :
      rows = []
      self.setPlaceHolder('filter', "")
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
        mark = self.params['mark'].value
        sql = SELECT + f" WHERE mark = '{mark}'"
        rows = self.__mysql.query(sql)
      else :
        # フィルタ指定がない(通常の)場合
        rows = self.__mysql.query(SELECT + " LIMIT 1000;")
      self.setPlaceHolder('result', "")
      # クエリー
      self.setPlaceHolder('result', self.getResult(rows))
      self.setPlaceHolder('message', "クエリー OK")
      if len(rows) == 0 :
        self.setPlaceHolder('message', "０件のデータが検出されました。")
    except Exception as e:
      self.setPlaceHolder('message', "致命的エラーを検出。" + str(e))

  # クエリー結果を表にする。
  def getResult(self, rows) :
    result = ""
    for row in rows :
      td = []
      td.append(row[0])
      td.append(row[1])
      title = f"<a href=\"playform.cgi?id={row[0]}\" target=\"_blank\">{row[2]}</a>"
      td.append(title)
      td.append(row[3])
      td.append(MainPage.setNoneToEmpty(row[4]))
      td.append(MainPage.setNoneToEmpty(row[5]))
      td.append(MainPage.setNoneToEmpty(row[6]))
      td.append(MainPage.setNoneToEmpty(row[7]))
      td.append(row[8])
      td.append(row[9])
      td.append(row[10])
      td.append(row[11])
      result += WebPage.table_row(td) + "\n"
    return result

  # SQL を作る。
  def makeFilterSql(self, filter) :
    sql = SELECT + f" WHERE `title` LIKE '%{filter}%' UNION "
    sql += SELECT + f" WHERE `path` LIKE '%{filter}%' UNION "
    sql += SELECT + f" WHERE `album` LIKE '%{filter}%' UNION "
    sql += SELECT + f" WHERE `info` LIKE '%{filter}%'"
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
