#!/usr/bin/python3
# -*- code=utf-8 -*-
#   MySQL-IS csv.cgi  Version 2.00
import WebPage as web
import MySQL
import Text
#from syslog import syslog


# CGI WebPage クラス
class MainPage(web.WebPage) :
  SAVEDIR = '/var/www/data'
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.__mysql = MySQL.MySQL()
    self.schema = self.conf['db']
    self.getTables()
    if self.isParam('submit') :
      # Postback
      self.tableName = self.getParam('tables')
      self.direction = self.getParam('direction')
      self.caption = False if self.getParam('caption') == "" else True
      self.separator = self.getParam('separator')
      # Export / Import ?
      try :
        if self.direction == "export" :
          self.exportTable()
        else :
          self.importTable()
      except Exception as e:
        self.setPlaceHolder('message', "Error: " + str(e))
        self.setPlaceHolder('result', '')
    else :
      # Non Postback
      self.setPlaceHolder('message', '')
      self.setPlaceHolder('result', '')
    return

  # テーブルのエクスポート
  def exportTable(self) :
    filename = MainPage.SAVEDIR + "/" + self.tableName
    if self.separator == "comma" :
      filename += ".csv"
      separator = ","
    else :
      filename += ".tsv"
      separator = "\t"
    sql = f"SELECT * FROM {self.tableName}"
    rows = self.__mysql.query(sql)
    with open(filename, "w", encoding="utf-8") as f :
      if self.caption :
        fields = self.__mysql.getFieldNames()
        s = Text.join(separator, fields)
        f.write(s + "\n")
      for row in rows :
        s = ""
        for i in range(len(row)) :
          s += str(row[i]) + separator
        s = s[0:len(s)-1] + "\n"
        f.write(s)
    message = 'データがエクスポートされました。 '
    message += "テーブル:"
    message += self.tableName
    message += ", 表題行:"
    message += ("あり" if self.caption else "なし")
    message += ", 区切り文字:"
    message +=  ("カンマ" if self.separator == "comma" else "タブ")
    self.setPlaceHolder('message', message)
    filebody = self.tableName + (".csv" if self.separator == "comma" else ".tsv")
    self.setPlaceHolder('result', f"<a href=\"/data/{filebody}\">{filebody}</a>")
    return
    
  # テーブルのインポート
  def importTable(self) :
    self.saveFile('file', MainPage.SAVEDIR)
    fileName = self.params['file'].filename
    tableName = self.tableName
    separator = "," if self.separator == "comma" else "\t"
    try :
      self.loadData(MainPage.SAVEDIR + "/" + fileName, tableName)
      message = "データがインポートされました。"
      message += "テーブル:"
      message += self.tableName
      message += ", 表題行:"
      message += ("あり" if self.caption else "なし")
      message += ", 区切り文字:"
      message +=  ("カンマ" if self.separator == "comma" else "タブ")
    except Exception as e :
      message = "Error: データのインポートに失敗しました。" + str(e)
    self.setPlaceHolder('message', message)
    self.setPlaceHolder('result', '')
    return

  # CSV ファイルをテーブルに書き込む。
  def loadData(self, filePath, tableName) :
    separator = "," if self.separator == "comma" else "\t"
    number = 1 if self.caption else 0
    sql = f"LOAD DATA LOCAL INFILE '{filePath}' INTO TABLE {tableName} FIELDS TERMINATED BY '{separator}' IGNORE {number} LINES"
    self.__mysql.execute(sql)
    # 履歴を取る。
    sqlquoted = sql.replace("'", "''")
    hist = f"INSERT INTO History(dtime,caption,content,application,tag,info) VALUES(cast(now() as datetime),'IMPORT TABLE','{sqlquoted}','MySQL-IS python3','2','IMPORT TABLE')"
    self.__mysql.execute(hist)
    return

  # テーブル一覧を得る。
  def getTables(self) :
    sql = f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE' AND TABLE_SCHEMA='{self.schema}'"
    rows = self.__mysql.query(sql)
    buff = ""
    for row in rows :
      tableName = row[0]
      buff += f"<option>{tableName}</option>"
    self.setPlaceHolder('tables', buff)
    return



# メイン開始位置
wp = MainPage('templates/csv.html')
wp.echo()
