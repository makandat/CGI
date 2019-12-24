#!/usr/bin/env python3
#!C:\Program Files (x86)\Python37\python.exe
# -*- code=utf-8 -*-
#   index.cgi  Version 3.76  2019-12-23 (listpics.cgi)
from WebPage import WebPage
from MySQL import MySQL
import FileSystem as fs
import Common
import Text

SELECT = 'SELECT id, title, creator, path, mark, info, fav, count, bindata FROM Pictures'
LIMIT = 200
VERSION = 3.76

# CGI WebPage クラス
class MainPage(WebPage) :

  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.setPlaceHolder('result', "")
    self.setPlaceHolder('images', "")
    self.setPlaceHolder('view', "icons")
    self.view = "detail"
    try :
      rows = []
      sql = ""
      self.setPlaceHolder('version', VERSION)
      self.setPlaceHolder('filter', "")
      self.setPlaceHolder('start_id', "")
      self.__mysql = MySQL()
      # テーブル情報を表示
      self.setPlaceHolder("tableInfo", self.tableInfo())
      # ページ処理
      self.setPlaceHolder('next', '')
      self.setPlaceHolder('prev', '')
      # フィルタ別処理
      if self.isParam('filter') :
        # フィルタ指定がある場合
        filter = self.getParam('filter')
        self.setPlaceHolder('filter', "[設定フィルタ] \"" + filter + '"　<a href="index.cgi">(リセット)</a>')
        sql = self.makeFilterSql(filter)
        rows = self.__mysql.query(sql)
        self.resetOrder()
      elif self.isParam('id') and self.isParam('dir') :
        # ページ処理
        id = int(self.getParam('id'))
        dir = self.getParam('dir')
        if self.isCookie('order') :
          order = self.getCookie('order')
        else :
          order = "DESC"
        if order == "ASC" :
          if dir == 'next' :
            sql = SELECT + f" WHERE id > {id} ORDER BY id ASC LIMIT {LIMIT}"
          else :
            id0 = id - LIMIT
            sql = SELECT + f" WHERE id > {id0} ORDER BY id ASC LIMIT {LIMIT}"
          self.setPlaceHolder("ASCchecked", "checked")
          self.setPlaceHolder("DESCchecked", "")
        else :
          if dir == 'next' :
            sql = SELECT + f" WHERE id < {id} ORDER BY id DESC LIMIT {LIMIT}"
          else :
            id0 = id + LIMIT
            sql = SELECT + f" WHERE id < {id0} ORDER BY id DESC LIMIT {LIMIT}"
          self.setPlaceHolder("ASCchecked", "")
          self.setPlaceHolder("DESCchecked", "checked")
        rows = self.__mysql.query(sql)
      elif self.isParam('creator') :
        self.setPlaceHolder("version", self.getParam('creator'))
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
        sql = SELECT + criteria
        rows = self.__mysql.query(sql)
        self.resetOrder()
      elif self.isParam("btnOrder") :
        # フォームのクエリー
        rows = self.btnOrder()
      elif self.isParam('view') :
        # アイコン・詳細表示
        view = self.getParam('view')
        order = ""
        if self.isCookie('order') :
          order = self.getCookie('order')
        else :
          order = "DESC"
          self.setCookie('order', 'DESC')
        self.resetOrder(order)
        if view == 'detail' :
          self.view = 'detail'
          self.setPlaceHolder('view', 'icons')
        else :
          self.view = 'icons'
          self.setPlaceHolder('view', 'detail')
        current = int(self.getCookie('next', '0'))
        order = self.getCookie('order', 'DESC')
        if order == 'ASC' :
          sql = SELECT + " WHERE id > {0} ORDER BY id LIMIT {1}".format(current, LIMIT)
        else :
          sql = SELECT + " WHERE id < {0} ORDER BY id DESC LIMIT {1}".format(current + LIMIT, LIMIT)
        rows = self.__mysql.query(sql)
      else :
        # フィルタ指定がない(通常の)場合
        rows = self.queryNormal()
      # end case
      n = len(rows) - 1
      self.setPlaceHolder('result', "")
      # クエリー結果を表示する。
      if self.view == 'icons' :
        result = self.getIcons(rows)
        self.setPlaceHolder('images', result)
        self.setPlaceHolder('result', '')
      else :
        result = self.getResult(rows)
        self.setPlaceHolder('result', result)
        self.setPlaceHolder('images', '')
      self.setPlaceHolder('message', "クエリー OK")
      if len(rows) == 0 :
        self.setPlaceHolder('message', "０件のデータが検出されました。")
    except Exception as e:
      (filename, lineno, line, exc_obj) = Common.errorInfo()
      self.setPlaceHolder('message', "致命的エラーを検出。<br />Filename={0}, <br />LineNo={1}, Line='{2}', <br />Message='{3}'".format(filename, lineno, line, exc_obj))
    return

  # 通常のクエリ(フィルタ指定なし)
  def queryNormal(self) :
    self.setPlaceHolder("start_id", "")
    sql = ""
    if self.isCookie('order') :
      self.order = self.getCookie("order")
      sql = SELECT + f" ORDER BY id {self.order} LIMIT {LIMIT};"
      rows = self.__mysql.query(sql)
      if self.order == "DESC" :
        self.setPlaceHolder("ASCchecked", "")
        self.setPlaceHolder("DESCchecked", "checked")
      else :
        self.setPlaceHolder("ASCchecked", "checked")
        self.setPlaceHolder("DESCchecked", "")
    else:
      sql = SELECT + f" ORDER BY id DESC LIMIT {LIMIT};"
      rows = self.__mysql.query(sql)
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
    sql = ''
    if self.order == "DESC" :
      sql = SELECT + f" WHERE id <= {self.start_id} ORDER BY id {self.order} LIMIT {LIMIT};"
      rows = self.__mysql.query(sql)
      self.setPlaceHolder("DESCchecked", "checked")
      self.setPlaceHolder("ASCchecked", "")
    else :
      sql = SELECT + f" WHERE id >= {self.start_id} ORDER BY id {self.order} LIMIT {LIMIT};"
      rows = self.__mysql.query(sql)
      self.setPlaceHolder("DESCchecked", "")
      self.setPlaceHolder("ASCchecked", "checked")
    return rows

  # クエリー結果を表にする。
  def getResult(self, rows) :
    result = "<tr><th>id</th><th>タイトル</th><th>作者</th><th>パス名</th><th>マーク</th><th>情報</th><th>好き</th><th>参照回数</th><th>イメージ</th></tr>"
    id0 = 0
    id = 0
    for row in rows :
      id = str(row[0])
      if id0 == 0 :
        id0 = id
      title = row[1]
      creator = row[2]
      path = row[3]
      mark = row[4]
      info = row[5]
      fav = str(row[6])
      count = str(row[7])
      bindata = str(row[8])
      row2 = list()
      #row2.append(f"<a href=\"modify.cgi?id={id}\">{id}</a>")
      row2.append(id)
      ext = fs.getExtension(path).upper()
      if ext == ".JPG" or ext == ".PNG" or ext == ".GIF" :
        row2.append("<a href=\"getImage.cgi?path={0}\" target=\"_blank\">{1}</a>".format(path, title))
      else :
        row2.append("<a href='listpics.cgi?id={0}' target='_blank'>{1}</a>".format(id, title))
      row2.append(f"<a href=\"index.cgi?creator={creator}\">{creator}</a>")
      row2.append(path)
      row2.append(mark)
      row2.append(info)
      row2.append(f"<a href=\"like.cgi?id={id}\" target=\"_blank\">{fav}</a>")
      row2.append(count)
      if row[8] == None :
        row2.append('')
      elif bindata == '0' :
        row2.append('0')
      else :
        link = f"<img src=\"extract.cgi?id={bindata}\" alt=\"{bindata}\" />"
        row2.append(link)
      result += WebPage.table_row(row2) + "\n"
    self.setPlaceHolder('next', id)
    self.setPlaceHolder('prev', id0)
    self.setCookie('next', id)
    self.setCookie('prev', id0)
    return result

  # アイコン一覧を作る。
  def getIcons(self, rows) :
    result = "<div>\n"
    id0 = 0
    id = 0
    for row in rows :
      id = str(row[0])
      if id0 == 0 :
        id0 = id
      title = row[1]
      creator = row[2]
      path = row[3]
      bindata = row[8]
      if bindata == 0 or bindata == None :
        img = "<img src=\"/img/NoImage.jpg\" />"
      else :
        img = "<img src=\"extract.cgi?id={0}\" />".format(bindata)
      imglink = "<a href=\"listpics.cgi?id={0}\" target=\"_blank\">{1}</a>".format(id, img)
      result += "<div style=\"display:inline-block;padding:6px;\">"
      result += imglink
      annotation = "[{0}] {1}".format(creator, title)
      annotation = Text.left(annotation, 16)
      result += WebPage.tag('div', annotation, 'style="font-size:10pt;"')
      result += "</div>\n"
    result += "</div>\n"
    self.setPlaceHolder('next', id)
    self.setPlaceHolder('prev', id0)
    self.setCookie('next', id)
    self.setCookie('prev', id0)
    return result

  # SQL を作る。 # 2019-10-04
  def makeFilterSql(self, filter) :
    filter = filter.replace("'", "''")
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
