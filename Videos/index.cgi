#!/usr/bin/env python3
# -*- code=utf-8 -*-
# Videos テーブルのテスト
#   MySQL を利用
import WebPage as page
import FileSystem as fsys
import MySQL

SELECT = 'SELECT id, title, path, mark, info, fav, count FROM Videos'

# CGI WebPage クラス
class MainPage(page.WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    try :
      self.__mysql = MySQL.MySQL()
      rows = self.__mysql.query(SELECT)
      self.vars['result'] = ""
      # クエリー
      self.vars['result'] = self.getResult(rows)
      self.vars['message'] = "クエリー OK"
    except Exception as e:
      self.vars['message'] = "致命的エラーを検出。" + str(e)

  # クエリー結果を表にする。
  def getResult(self, rows) :
    result = ""
    for row in rows :
      result += page.WebPage.table_row(row) + "\n"
    return result

# メイン開始位置
wp = MainPage('templates/index.html')
wp.echo()
