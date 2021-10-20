#!C:\python3\python.exe
#!/usr/bin/python3
# -*- code=utf-8 -*-
# Pictures テーブルのデータ追加・修正  v3.86  2020-03-29
#   MySQL を利用
from WebPage import WebPage
import FileSystem as fs
from MySQL import MySQL
import Common
import Text
#from syslog import syslog

SELECT = "SELECT album, title, creator, path, mark, info, fav, count, bindata FROM Pictures WHERE id = {0}"
INSERT = "INSERT INTO Pictures(album, title, creator, path, mark, info, fav, count, `date`, sn) VALUES({0}, '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', {7}, CURRENT_DATE(), {8})"
INSERT2 = "INSERT INTO Pictures(album, title, creator, path, mark, info, fav, count, bindata, `date`, sn) VALUES({0}, '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', {7}, {8}, CURRENT_DATE(), {9})"
UPDATE = "UPDATE Pictures SET album={1}, title='{2}', creator='{3}', path='{4}', mark='{5}', info='{6}', fav={7}, count={8}, bindata={9}, `date`=CURRENT_DATE() WHERE id={0};"

# CGI WebPage クラス
class MainPage(WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    #Common.init_logger('/home/user/logs/Pictures.log')
    try :
      self.client = MySQL()
      if self.isParam('id') and not (self.isParam('btnAdd') or self.isParam('btnQuery')) :
        self.query()
      elif self.isParam('btnAdd') :
        # 追加・修正ボタンのとき
        if self.isParam('id') :
          # id が指定されている場合
          self.modify()
        else :
          # id が指定されていない場合
          self.add()
      elif self.isParam('btnQuery') :
        # データ確認ボタンの時
        if self.isParam('id') :
          self.query()
        else :
          # id が指定されていない場合
          self.clearAll()
          self.setPlaceHolder('message', "id が指定されていません。")
      else :
        # その他の場合
        self.clearAll()
        self.setPlaceHolder('message', "")
    except Exception as e:
      self.clearAll()
      self.setPlaceHolder('message', "致命的エラーを検出。" + str(e))
    return

  # データ修正
  def modify(self) :
    try :
      id = self.getParam('id')
      album = self.getParam('album')
      title = Text.replace("'", "''", self.getParam('title'))
      path = Text.replace("'", "''", self.getParam('path'))
      path = Text.replace("\\", "/", path)
      path = Text.trim(path)
      creator = Text.replace("'", "''", self.getParam('creator'))
      mark = self.getParam('mark')
      info = self.getParam('info')
      fav = self.getParam('fav')
      count = self.getParam('count')
      bindata = self.getParam('bindata')
      if title == "" or path == "" or title == None or path == None :
        self.setPlaceHolder('message', "修正 NG : タイトルまたはパスが空欄です。")
        self.setPlaceHolder('id', "")
        self.setPlaceHolder('album', album)
        self.setPlaceHolder('title', title)
        self.setPlaceHolder('creator', creator)
        self.setPlaceHolder('path', path)
        self.setPlaceHolder('mark', MainPage.setNoneToEmpty(mark))
        self.setPlaceHolder('info', MainPage.setNoneToEmpty(info))
        self.setPlaceHolder('fav', str(fav))
        self.setPlaceHolder('count', str(count))
        self.setPlaceHolder('bindata', MainPage.setNoneToEmpty(bindata))
        return
      if bindata == '' :
        bindata = 0
      sql = Text.format(UPDATE, id, album, title, creator, path, mark, info, fav, count, bindata)
      self.client.execute(sql)
      self.setPlaceHolder('id', id);
      self.setPlaceHolder('album', album);
      self.setPlaceHolder('title', title)
      self.setPlaceHolder('creator', creator)
      self.setPlaceHolder('path', path)
      self.setPlaceHolder('mark', MainPage.setNoneToEmpty(mark))
      self.setPlaceHolder('info', MainPage.setNoneToEmpty(info))
      self.setPlaceHolder('fav', str(fav))
      self.setPlaceHolder('count', str(count))
      self.setPlaceHolder('bindata', MainPage.setNoneToEmpty(bindata))
      self.setPlaceHolder('message', f"id={id} 修正 OK.  <a href=\"listpics.cgi?id={id}\">見る</a>")
    except Exception as e:
      self.setPlaceHolder('message', f"id={id} 修正 NG : " + str(e))
      self.clearAll()
    return

  # データ追加
  def add(self) :
    try :
      #Common.log("add(self)")
      album = self.getParam('album')
      title = Text.replace("'", "''", self.getParam('title'))
      path = Text.replace("'", "''", self.getParam('path'))
      path = Text.replace("\\", "/", path)
      path = Text.trim(path)
      if self.checkPath(path) == False :
        self.clearAll()
        return
      creator = Text.replace("'", "''", self.getParam('creator'))
      mark = self.getParam('mark')
      info = self.getParam('info')
      fav = self.getParam('fav')
      count = self.getParam('count')
      bindata = self.getParam('bindata')
      #Common.log("sn = self.getNextSN()")
      sn = self.getNextSN()
      #Common.log("sn="+str(sn))
      if title == "" or path == "" or title == None or path == None :
        self.setPlaceHolder('message', "追加 NG : タイトルまたはパスが空欄です。")
        self.setPlaceHolder('id', "")
        self.setPlaceHolder('album', album)
        self.setPlaceHolder('title', title)
        self.setPlaceHolder('creator', creator)
        self.setPlaceHolder('path', path)
        self.setPlaceHolder('mark', MainPage.setNoneToEmpty(mark))
        self.setPlaceHolder('info', MainPage.setNoneToEmpty(info))
        self.setPlaceHolder('fav', str(fav))
        self.setPlaceHolder('count', str(count))
        self.setPlaceHolder('bindata', MainPage.setNoneToEmpty(bindata))
        return
      if bindata == '' :
        sql = INSERT.format(album, title, creator, path, mark, info, fav, count, sn)
      else :
        sql = INSERT2.format(album, title, creator, path, mark, info, fav, count, bindata, sn)
      #Common.log(sql)
      self.client.execute(sql)
      self.setPlaceHolder('id', "")
      self.setPlaceHolder('album', album)
      self.setPlaceHolder('title', title)
      self.setPlaceHolder('creator', creator)
      self.setPlaceHolder('path', path)
      self.setPlaceHolder('mark', MainPage.setNoneToEmpty(mark))
      self.setPlaceHolder('info', MainPage.setNoneToEmpty(info))
      self.setPlaceHolder('fav', str(fav))
      self.setPlaceHolder('count', str(count))
      self.setPlaceHolder('bindata', MainPage.setNoneToEmpty(bindata))
      maxid = self.client.getValue("SELECT max(id) FROM Pictures")
      self.setPlaceHolder('message', f"追加 {maxid} OK.  <a href=\"listpics.cgi?id={maxid}\">見る</a>")
    except Exception as e:
      self.setPlaceHolder('message', "追加 NG : " + str(e))
      self.clearAll()
    return

  # 次の sn を得る。
  def getNextSN(self) :
    sn = self.client.getValue("SELECT max(sn) FROM Pictures")
    if sn == None :
      return 1
    return sn + 1

  # パスのチェック
  def checkPath(self, path) :
    if fs.exists(path) == False :
      self.setPlaceHolder('message', path + " は存在しません。")
      return False
    n = self.client.getValue(f"SELECT count(*) FROM Pictures WHERE path='{path}'")
    if n > 0 :
      self.setPlaceHolder('message', path + " は登録済みです。")
      return False
    return True

  # データ取得
  def query(self) :
    try :
      sql = SELECT.format(self.getParam('id'))
      rows = self.client.query(sql)
      if len(rows) > 0 :
        row = rows[0]
        id = self.getParam('id')
        self.setPlaceHolder('id', id)
        self.setPlaceHolder('album', row[0])
        self.setPlaceHolder('title', row[1].replace("'", '&#39'))
        self.setPlaceHolder('creator', row[2].replace("'", '&#39'))
        self.setPlaceHolder('path', row[3].replace("'", '&#39'))
        self.setPlaceHolder('mark', MainPage.setNoneToEmpty(row[4]))
        self.setPlaceHolder('info', MainPage.setNoneToEmpty(row[5]))
        self.setPlaceHolder('fav', row[6])
        self.setPlaceHolder('count', row[7])
        self.setPlaceHolder('bindata', MainPage.setNoneToEmpty(row[8]))
        self.setPlaceHolder('message', f"クエリー id={id} OK")
      else :
        self.clearAll(int(self.getParam('id')))
        self.setPlaceHolder('message', f"クエリー id={id} NG : Bad id.")
    except Exception as e :
      self.clearAll(int(self.getParam('id')))
      self.setPlaceHolder['message'] = f"クエリー NG : id={id}. " + str(e)
    return

  # フォームのフィールドをクリアする。
  def clearAll(self, id = -1) :
    if id < 0 :
      self.setPlaceHolder('id', "")
    else :
      self.setPlaceHolder('id', str(id))
    self.setPlaceHolder('album', "0")
    self.setPlaceHolder('title', "")
    self.setPlaceHolder('path', "")
    self.setPlaceHolder('creator', "")
    self.setPlaceHolder('mark', "")
    self.setPlaceHolder('info', "")
    self.setPlaceHolder('fav', "0")
    self.setPlaceHolder('count', "0")
    self.setPlaceHolder('bindata', "0")
    return

  # 引数が None の場合、"" に変換する。
  @staticmethod
  def setNoneToEmpty(v) :
    if v == None :
      return ""
    else :
      return v

# メイン開始位置
wp = MainPage('templates/modify.html')
wp.echo()
