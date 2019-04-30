#!/usr/bin/env python3
#!C:\Program Files (x86)\Python37\python.exe
# -*- code=utf-8 -*-
#   MySQL-IS index.cgi  Version 2.10  2019-04-31
import WebPage as web
import MySQL
import Text
import Common
#from syslog import syslog


# CGI WebPage クラス
class MainPage(web.WebPage) :

  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.__mysql = MySQL.MySQL()
    self.setPlaceHolder('schema', self.conf['db'])
    self.setPlaceHolder('userid', self.conf['uid'])
    #Common.init_logger('c:/temp/Logger.log')
    if self.isParam("menu") :
      menu = self.getParam('menu')
      if menu == "users" :
        # ユーザ一覧
        rows = self.listUsers()
        self.showRows(rows, ['GRANTEE'])
        self.setPlaceHolder('title', 'ユーザ一覧')
      elif menu == "tables" :
        # テーブル一覧
        rows = self.listTables()
        self.showRows(rows, ['TABLE_NAME', 'DATA_LENGTH', 'AUTO_INCREMENT', 'CREATE_TIME', 'UPDATE_TIME'], "columns")
        self.setPlaceHolder('title', 'テーブル一覧')
      elif menu == "views" :
        # ビュー一覧
        rows = self.listViews()
        self.showRows(rows, ['TABLE_NAME'], "viewdef")
        self.setPlaceHolder('title', 'ビュー一覧')
      elif menu == "indexes" :
        # インデックス一覧
        rows = self.listIndexes()
        self.showRows(rows, ['INDEX_NAME', 'TABLE_NAME', 'COLUMN_NAME', 'SEQ_IN_INDEX'], "indexdef")
        self.setPlaceHolder('title', 'インデックス一覧')
      elif menu == "routines" :
        # ルーチン一覧
        rows = self.listRoutines()
        self.showRows(rows, ['ROUTINE_NAME', 'ROUTINE_TYPE', 'DATA_TYPE'], "routinedef")
        self.setPlaceHolder('title', 'ルーチン一覧')
      elif menu == "triggers" :
        # トリガ一覧
        rows = self.listTriggers()
        self.showRows(rows, ['TRIGGER_NAME', 'EVENT_MANIPULATION', 'ACTION_TIMING'], "triggerdef")
        self.setPlaceHolder('title', 'トリガ一覧')
      elif menu == "characters" :
        # 文字コード一覧
        rows = self.listCharacterSet()
        self.showRows(rows, ['CHARACTER_SET_NAME', 'DEFAULT_COLLATE_NAME', 'DESCRIPTION', 'MAXLEN'])
        self.setPlaceHolder('title', '文字コード一覧')
      elif menu == "collations" :
        # 並び順一覧
        rows = self.listCollation()
        self.showRows(rows, ['COLLATION_NAME', 'CHARACTER_SET_NAME', 'ID', 'IS_DEFAULT'])
        self.setPlaceHolder('title', '並び順一覧')
      elif menu == "columns" :
        # テーブルのカラム一覧
        tableName = self.getParam('name')
        rows = self.getColumns(tableName)
        self.showRows(rows, ['ORDINAL_POSITION', 'COLUMN_NAME', 'COLUMN_DEFAULT', 'IS_NULLABLE', 'COLUMN_TYPE', 'COLUMN_KEY', 'EXTRA'])
        self.setPlaceHolder('title', tableName + ' カラム一覧')
      elif menu == "viewdef" :
        viewName = self.getParam('name')
        rows = self.getViewDef(viewName)
        self.showText(rows)
        self.setPlaceHolder('title', viewName + ' の定義')
      elif menu == "routinedef" :
        routine = self.getParam('name')
        rows = self.getRoutineDef(routine)
        if len(rows) == 0 :
          self.setPlaceHolder('content', '<tr><td>ルーチン見つかりません。</td></tr>')
          self.setPlaceHolder('title', routine + ' の定義')
          return
        row = rows[0]
        param_list = row[0]
        returns = row[1]
        body = row[2]
        self.showRoutine(param_list, returns, body)
        self.setPlaceHolder('title', routine + ' の定義')
      elif menu == "triggerdef" :
        trigger = self.getParam('name')
        rows = self.getTriggerDef(trigger)
        if len(rows) == 0 :
          self.setPlaceHolder('content', '<tr><td>トリガが見つかりません。</td></tr>')
          self.setPlaceHolder('title', trigger + ' の定義')
          return
        #Common.log("menu=triggerdef")
        row = rows[0]
        tigger_name = trigger
        #Common.log(tigger_name)
        event_manipulation = row[0]
        #Common.log(event_manipulation)
        action_timing = row[1]
        #Common.log(action_timing)
        action_statement = row[2]
        #Common.log(action_statement)
        self.showTrigger(tigger_name, event_manipulation, action_timing, action_statement)
        self.setPlaceHolder('title', trigger + ' の定義')
      else :
        # データベース一覧
        rows = self.listDatabases()
        self.showRows(rows, ['SCHEMA_NAME', 'DEFAULT_CHARACTER_SET_NAME', 'DEFAULT_COLLATION_NAME'])
        self.setPlaceHolder('title', 'データベース一覧')
    else :
        # データベース一覧
      rows = self.listDatabases()
      self.showRows(rows, ['SCHEMA_NAME', 'DEFAULT_CHARACTER_SET_NAME', 'DEFAULT_COLLATION_NAME'])
      self.setPlaceHolder('title', 'データベース一覧')
    return


  # 行列を表示する。
  def showRows(self, rows, names, alink="") :
    content = "<tr>"
    i = 0
    # HTML テーブルの表題部分
    for name in names :
      content += "<th>"
      content += names[i]
      content += "</th>"
      i += 1
    content += "</tr>\n"
    # HTML テーブルの内容部分
    for row in rows :
      content += "<tr>"
      for i in range(len(names)) :
        content += "<td>"
        if i == 0 :
          content += self.makelink(str(row[i]), alink)
        else :
          s = str(row[i])
          if s == 'None' :
            s = 'NULL'
          else :
            pass
          content += s
        content += "</td>"
      content += "</tr>\n"
    self.setPlaceHolder('content', content)
    return

  # テキストを表示
  def showText(self, rows) :
    content = "<pre style='margin-left:30px;'>"
    for row in rows :
      c = row[0]
      if c == "&" :
        c = "&amp;"
      if c == "<" :
        c = "&lt;"
      content += c
      if len(content) % 160 == 0:
        content += "\n"
    self.setPlaceHolder('content', content)
    return

  # ルーチンの内容を表示 (PARAM_LIST, RETURNS, BODY)
  def showRoutine(self, param_list, returns, body) :
    content = "<tr><td><b>PARAM_LIST : </b><br />"
    content += str(param_list) if param_list != None else ""
    content += "<br /><b>RETURNS : </b><br />"
    content += str(returns) if returns != None else ""
    content += "<br /><b>BODY : </b><br />"
    content += str(body).replace("\\r", "<br />") if body != None else ""
    content += "</td></tr>"
    self.setPlaceHolder('content', content)
    return

  # トリガの内容を表示 (TRIGGER_NAME, EVENT_MANIPULATION, ACTION_TIMING)
  def showTrigger(self, trigger_name, event_manipulation, action_timing, action_statement) :
    content = "<tr><td><b>TRIGGER_NAME : </b><br />"
    content += str(trigger_name)
    content += "<br /><b>EVENT_MANIPULATION : </b><br />"
    content += str(event_manipulation)
    content += "<br /><b>ACTION_TIMING : </b><br />"
    content += str(action_timing)
    content += "<br /><b>ACTION_STATEMENT : </b><br />"
    content += str(action_statement.replace("\\r", "<br />")) if action_statement != None else ""
    content += "</td></tr>"
    self.setPlaceHolder('content', content)
    return


  # alink に従ってアンカーを作る。
  def makelink(self, text, alink="") :
    if alink == 'columns' :
      s = f"<a href=\"index.cgi?menu=columns&name={text}\">{text}</a>"
    elif alink == 'viewdef' :
      s = f"<a href=\"index.cgi?menu=viewdef&name={text}\">{text}</a>"
      #elif alink == 'indexdef' and text != "PRIMARY" :
      #  s = f"<a href=\"index.cgi?menu=indexdef&name={text}\">{text}</a>"
    elif alink == 'routinedef' :
      s = f"<a href=\"index.cgi?menu=routinedef&name={text}\">{text}</a>"
    elif alink == 'triggerdef' :
      s = f"<a href=\"index.cgi?menu=triggerdef&name={text}\">{text}</a>"
    else :
      s = text
    return s

  # データベース一覧を得る。
  def listDatabases(self) :
    sql = "SELECT SCHEMA_NAME, DEFAULT_CHARACTER_SET_NAME, DEFAULT_COLLATION_NAME FROM INFORMATION_SCHEMA.SCHEMATA ORDER BY SCHEMA_NAME"
    rows = self.__mysql.query(sql)
    return rows

  # ユーザ一覧を得る。
  def listUsers(self) :
    sql = "SELECT DISTINCT GRANTEE FROM INFORMATION_SCHEMA.USER_PRIVILEGES ORDER BY GRANTEE"
    rows = self.__mysql.query(sql)
    return rows

  # テーブル一覧
  def listTables(self) :
    schema = self.conf['db']
    sql = f"SELECT TABLE_NAME, DATA_LENGTH, AUTO_INCREMENT, CREATE_TIME, UPDATE_TIME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE' AND TABLE_SCHEMA='{schema}'"
    rows = self.__mysql.query(sql)
    return rows

  # ビュー一覧
  def listViews(self) :
    schema = self.conf['db']
    sql = f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.VIEWS WHERE TABLE_SCHEMA='{schema}'"
    rows = self.__mysql.query(sql)
    return rows

  # インデックス一覧
  def listIndexes(self) :
    schema = self.conf['db']
    sql = f"SELECT INDEX_NAME, TABLE_NAME, COLUMN_NAME, SEQ_IN_INDEX FROM INFORMATION_SCHEMA.STATISTICS WHERE INDEX_SCHEMA='{schema}'"
    indexes = self.__mysql.query(sql)
    return indexes;

  # ルーチン一覧
  def listRoutines(self) :
    schema = self.conf['db']
    sql = f"SELECT ROUTINE_NAME, ROUTINE_TYPE, DATA_TYPE FROM INFORMATION_SCHEMA.ROUTINES WHERE ROUTINE_SCHEMA='{schema}'"
    rows = self.__mysql.query(sql)
    return rows

  # トリガ一覧
  def listTriggers(self) :
    schema = self.conf['db']
    sql = f"SELECT TRIGGER_NAME, EVENT_MANIPULATION, ACTION_TIMING FROM INFORMATION_SCHEMA.TRIGGERS WHERE TRIGGER_SCHEMA='{schema}'"
    rows = self.__mysql.query(sql)
    return rows

  # 文字セット一覧
  def listCharacterSet(self) :
    sql = "SELECT CHARACTER_SET_NAME, DEFAULT_COLLATE_NAME, DESCRIPTION, MAXLEN FROM INFORMATION_SCHEMA.CHARACTER_SETS"
    rows = self.__mysql.query(sql)
    return rows

  # 並び順一覧
  def listCollation(self) :
    sql = "SELECT COLLATION_NAME, CHARACTER_SET_NAME, ID, IS_DEFAULT FROM INFORMATION_SCHEMA.COLLATIONS"
    rows = self.__mysql.query(sql)
    return rows

  # ビューの定義を得る。
  def getViewDef(self, view) :
    schema = self.conf['db']
    sql = f"SELECT VIEW_DEFINITION FROM INFORMATION_SCHEMA.VIEWS WHERE TABLE_SCHEMA='{schema}' AND TABLE_NAME='{view}'"
    rows = self.__mysql.query(sql)
    if len(rows) > 0 :
      row = rows[0]
      return row[0]
    else :
      return ''

  # ルーチンの定義を得る。
  def getRoutineDef(self, routine) :
    schema = self.conf['db']
    sql = f"SELECT PARAM_LIST, RETURNS, BODY FROM mysql.proc WHERE DB='{schema}' AND NAME='{routine}'"
    result = self.__mysql.query(sql)
    return result

  # トリガの定義を得る。
  def getTriggerDef(self, trigger) :
    schema = self.conf['db']
    sql = f"SELECT EVENT_MANIPULATION, ACTION_TIMING, ACTION_STATEMENT FROM INFORMATION_SCHEMA.TRIGGERS WHERE TRIGGER_SCHEMA='{schema}' AND TRIGGER_NAME='{trigger}'"
    result = self.__mysql.query(sql)
    return result;

  # カラム一覧を得る。
  def getColumns(self, tableName) :
    schema = self.conf['db']
    sql = f"SELECT ORDINAL_POSITION, COLUMN_NAME, COLUMN_DEFAULT, IS_NULLABLE, COLUMN_TYPE, COLUMN_KEY, EXTRA FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='{schema}' AND TABLE_NAME='{tableName}'";
    columns = self.__mysql.query(sql)
    return columns

 

# メイン開始位置
wp = MainPage('templates/index.html')
wp.echo()
