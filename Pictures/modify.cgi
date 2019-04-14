#!C:\Program Files (x86)\Python37\python.exe
# -*- code=utf-8 -*-
# Pictures テーブルのデータ追加・修正  v1.02  2019-04-08
#   MySQL を利用
import WebPage as page
import FileSystem as fs
import MySQL
import Common
import Text
#from syslog import syslog

SELECT = "SELECT title, creator, path, mark, info, fav, count FROM Pictures WHERE id = {0}"
INSERT = "INSERT INTO Pictures(title, creator, path, mark, info, fav, count) VALUES('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', {6})"
UPDATE = "UPDATE Pictures SET title='{1}', creator='{2}', path='{3}', mark='{4}', info='{5}', fav='{6}', count={7} WHERE id={0};"

# CGI WebPage クラス
class MainPage(page.WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    try :
      self.client = MySQL.MySQL()
      if self.isParam('btnAdd') :
        # 追加・修正ボタンのとき
        if self.isParam('id') :
          # id が指定されている場合
          self.modify()
        else :
          # id が指定されていない場合
          self.add()
      elif self.isParam('btnQuery') :
        # データ確認ボタンの時
        self.query()
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
    rb = True
    try :
      id = self.getParam('id')
      title = Text.replace("'", "''", self.getParam('title'))
      path = Text.replace("'", "''", self.getParam('path'))
      path = Text.replace("\\", "/", path)
      creator = Text.replace("'", "''", self.getParam('creator'))
      mark = self.getParam('mark')
      info = self.getParam('info')
      fav = self.getParam('fav')
      count = self.getParam('count')
      if title == "" or path == "" or title == None or path == None :
        self.setPlaceHolder('message', "修正 NG : タイトルまたはパスが空欄です。")
        self.setPlaceHolder('id', "")
        self.setPlaceHolder('title', title)
        self.setPlaceHolder('creator', creator)
        self.setPlaceHolder('path', path)
        self.setPlaceHolder('mark', MainPage.setNoneToEmpty(mark))
        self.setPlaceHolder('info', MainPage.setNoneToEmpty(info))
        self.setPlaceHolder('fav', str(fav))
        self.setPlaceHolder('count', str(count))
        return
      sql = Text.format(UPDATE, id, title, creator, path, mark, info, fav, count)
      self.client.execute(sql)
      self.setPlaceHolder('id', id);
      self.setPlaceHolder('title', title)
      self.setPlaceHolder('creator', creator)
      self.setPlaceHolder('path', path)
      self.setPlaceHolder('mark', MainPage.setNoneToEmpty(mark))
      self.setPlaceHolder('info', MainPage.setNoneToEmpty(info))
      self.setPlaceHolder('fav', str(fav))
      self.setPlaceHolder('count', str(count))
      self.setPlaceHolder('message', f"修正 OK.  <a href=\"listpics.cgi?id={id}\">見る</a>")
    except Exception as e:
      self.setPlaceHolder('message', "修正 NG : " + str(e))
      self.clearAll()
    return

  # データ追加
  def add(self) :
    rb = True
    try :
      title = Text.replace("'", "''", self.getParam('title'))
      path = Text.replace("'", "''", self.getParam('path'))
      path = Text.replace("\\", "/", path)
      if self.checkPath(path) == False :
        self.clearAll()
        return
      creator = Text.replace("'", "''", self.getParam('creator'))
      mark = self.getParam('mark')
      info = self.getParam('info')
      fav = self.getParam('fav')
      count = self.getParam('count')
      if title == "" or path == "" or title == None or path == None :
        self.setPlaceHolder('message', "追加 NG : タイトルまたはパスが空欄です。")
        self.setPlaceHolder('id', "")
        self.setPlaceHolder('title', title)
        self.setPlaceHolder('creator', creator)
        self.setPlaceHolder('path', path)
        self.setPlaceHolder('mark', MainPage.setNoneToEmpty(mark))
        self.setPlaceHolder('info', MainPage.setNoneToEmpty(info))
        self.setPlaceHolder('fav', str(fav))
        self.setPlaceHolder('count', str(count))
        return
      sql = INSERT.format(title, creator, path, mark, info, fav, count)
      self.client.execute(sql)
      self.setPlaceHolder('id', "")
      self.setPlaceHolder('title', title)
      self.setPlaceHolder('creator', creator)
      self.setPlaceHolder('path', path)
      self.setPlaceHolder('mark', MainPage.setNoneToEmpty(mark))
      self.setPlaceHolder('info', MainPage.setNoneToEmpty(info))
      self.setPlaceHolder('fav', str(fav))
      self.setPlaceHolder('count', str(count))
      maxid = self.client.getValue("SELECT max(id) FROM Pictures")
      self.setPlaceHolder('message', f"追加 OK.  <a href=\"listpics.cgi?id={maxid}\">見る</a>")
    except Exception as e:
      self.setPlaceHolder('message', "追加 NG : " + str(e))
      self.clearAll()
    return


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
        self.setPlaceHolder('id', self.getParam('id'))
        self.setPlaceHolder('title', row[0])
        self.setPlaceHolder('creator', row[1])
        self.setPlaceHolder('path', row[2])
        self.setPlaceHolder('mark', MainPage.setNoneToEmpty(row[3]))
        self.setPlaceHolder('info', MainPage.setNoneToEmpty(row[4]))
        self.setPlaceHolder('fav', row[5])
        self.setPlaceHolder('count', row[6])
        self.setPlaceHolder('message', "クエリー OK")
      else :
        self.clearAll(int(self.getParam('id')))
        self.setPlaceHolder('message', "クエリー NG : Bad id.")
    except Exception as e :
      self.clearAll(int(self.getParam('id')))
      self.setPlaceHolder['message'] = "クエリー NG : " + str(e)
    return

  # フォームのフィールドをクリアする。
  def clearAll(self, id = -1) :
    if id < 0 :
      self.setPlaceHolder('id', "")
    else :
      self.setPlaceHolder('id', str(id))
    self.setPlaceHolder('title', "")
    self.setPlaceHolder('path', "")
    self.setPlaceHolder('creator', "")
    self.setPlaceHolder('mark', "")
    self.setPlaceHolder('info', "")
    self.setPlaceHolder('fav', "0")
    self.setPlaceHolder('count', "0")
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
