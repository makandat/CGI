#!C:\Program Files\Python3\python.exe
#!/usr/bin/env python3
# -*- code=utf-8 -*-
# Videos テーブルのデータ追加・修正 modify.cgi  ver1.60 2019-10-08
#   MySQL を利用
from WebPage import WebPage
import FileSystem as fs
from MySQL import MySQL
import Common
import Text
#from syslog import syslog

SELECT = "SELECT title, path, media, series, mark, info, fav, count, bindata, album FROM Videos WHERE id = {0}"
INSERT = "INSERT INTO Videos(title, path, media, series, mark, info, fav, count, bindata, album, folder) VALUES('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', {6}, {7}, {8}, {9}, '{10}')"
UPDATE = "UPDATE Videos SET title='{1}', path='{2}', media='{3}', series='{4}', mark='{5}', info='{6}', fav={7}, count={8}, bindata={9}, album={10} WHERE id={0};"

# CGI WebPage クラス
class MainPage(WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    #Common.init_logger('/var/www/data/Logger.log')
    try :
      self.client = MySQL()
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
      self.setPlaceHolder('message', "致命的エラーを検出。" + str(e))
    return

  # データ修正
  def modify(self) :
    try :
      id = self.getParam('id')
      title = self.getParam('title')
      path = self.getParam('path').replace("\\", "/")
      media = self.getParam('media')
      series = self.getParam('series')
      mark = self.getParam('mark')
      info = self.getParam('info')
      fav = self.getParam('fav')
      count = self.getParam('count')
      bindata = self.getParam('bindata')
      album = self.getParam('album')
      if title == "" or path == "" :
        self.setPlaceHolder('message', "修正 NG : タイトルまたはパスが空欄です。")
        self.embed({'id':id, 'title':self.getParam('title'), 'path':self.getParam('path'), 'media':media, 'series':series, 'mark':mark, 'info':info, 'fav':fav, 'count':count, 'bindata':bindata, 'album':album})
        return
      sql = UPDATE.format(id, title, path, media, series, mark, info, fav, count, bindata, album)
      self.client.execute(sql)
      self.embed({'id':id, 'title':self.getParam('title'), 'path':self.getParam('path'), 'media':media, 'series':series, 'mark':mark, 'info':info, 'fav':fav, 'count':count, 'bindata':bindata, 'album':album})
      self.setPlaceHolder('message', f"id={id} 修正 OK")
    except Exception as e:
      self.setPlaceHolder('message', "修正 NG : " + str(e))
      self.clearAll()
    return

  # データ追加
  def add(self) :
    try :
      id = ""
      title = Text.replace("'", "''", self.getParam('title'))
      path = Text.replace("\\", "/", self.getParam('path'))
      media = self.getParam('media')
      series = self.getParam('series')
      mark = self.getParam('mark')
      info = self.getParam('info')
      fav = self.getParam('fav')
      count = self.getParam('count')
      bindata = self.getParam('bindata')
      album = self.getParam('album')
      folder = '1' if fs.isDirectory(self.getParam('path')) else '0';
      if title == "" or path == "" :
        self.setPlaceHolder('message', "追加 NG : タイトルまたはパスが空欄です。")
        self.embed({'id':id, 'title':self.getParam('title'), 'path':self.getParam('path'), 'media':media, 'series':series, 'mark':mark, 'info':info, 'fav':fav, 'count':count, 'bindata':bindata, 'album':album})
        return
      sql = INSERT.format(title, path, media, series, mark, info, fav, count, bindata, album, folder)
      self.client.execute(sql)
      self.embed({'id':id, 'title':self.getParam('title'), 'path':self.getParam('path'), 'media':media, 'series':series, 'mark':mark, 'info':info, 'fav':fav, 'count':count, 'bindata':bindata, 'album':album})
      self.setPlaceHolder('message', title + " 追加 OK")
    except Exception as e:
      self.setPlaceHolder('message', "追加 NG : " + str(e))
      self.embed({'id':id, 'title':self.getParam('title'), 'path':self.getParam('path'), 'media':media, 'series':series, 'mark':mark, 'info':info, 'fav':fav, 'count':count, 'bindata':bindata, 'album':album})
    return

  # データ取得
  def query(self) :
    try :
      id = self.getParam('id')
      sql = SELECT.format(id)
      rows = self.client.query(sql)
      if len(rows) > 0 :
        row = rows[0]
        media = MainPage.setNoneToEmpty(row[2])
        series = MainPage.setNoneToEmpty(row[3])
        mark = MainPage.setNoneToEmpty(row[4])
        info = MainPage.setNoneToEmpty(row[5])
        self.embed({'id':id, 'title':row[0], 'path':row[1], 'media':media, 'series':series, 'mark':mark, 'info':info, 'fav':row[6], 'count':row[7], 'bindata':row[8], 'album':row[9]})
        self.setPlaceHolder('message', f"id={id} クエリー OK")
      else :
        self.clearAll(int(id))
        self.setPlaceHolder('message', "クエリー NG : Bad id.")
    except Exception as e :
      self.clearAll(int(id))
      self.setPlaceHolder('message', "クエリー NG : " + str(e))
    return

  # フォームのフィールドをクリアする。
  def clearAll(self, id = -1) :
    id2 = str(id)
    if id < 0 :
      id2 = ""
    self.embed({'id':id2, 'title':'', 'path':'', 'media':'', 'series':'', 'mark':'', 'info':'', 'fav':0, 'count':0, 'bindata':0, 'album':0})
    return
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
