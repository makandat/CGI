#!/usr/bin/env python3
#!C:\Program Files (x86)\Python37\python.exe
# -*- code=utf-8 -*-
# Music テーブルのデータ追加・修正 (modify.cgi)
#   MySQL を利用
from WebPage import WebPage
import FileSystem as fs
from MySQL import MySQL
import Common
import Text
#from syslog import syslog

SELECT = "SELECT title, path, artist, album, mark, info, fav, count, bindata, alindex FROM Music WHERE id = {0}"
INSERT = "INSERT INTO Music(title, path, artist, album, mark, info, fav, count, bindata, alindex) VALUES('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', {7}, {8}, {9})"
UPDATE = "UPDATE Music SET title='{1}', path='{2}', artist='{3}', album='{4}', mark='{5}', info='{6}', fav='{7}', count={8}, bindata={9}, alindex={10} WHERE id={0};"

# CGI WebPage クラス
class MainPage(WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    Common.init_logger('C:/temp/Logger.log')
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
      title = Text.replace("'", "''", self.getParam('title'))
      path = Text.replace("'", "''", self.getParam('path').replace("\\", "/"))
      artist = MainPage.setNoneToEmpty(self.getParam('artist'))
      album = MainPage.setNoneToEmpty(self.getParam('album'))
      mark = MainPage.setNoneToEmpty(self.getParam('mark'))
      info = MainPage.setNoneToEmpty(self.getParam('info'))
      fav = self.getParam('fav')
      count = self.getParam('count')
      bindata = self.getParam('bindata')
      alindex = self.getParam('alindex')
      dict1 = {'id':id, 'title':title, 'path':path, 'artist':artist, 'album':album, 'mark':mark, 'info':info, 'fav':fav, 'count':count, 'bindata':bindata, 'alindex':alindex}
      if title == "" or path == "" or title == None or path == None :
        self.setPlaceHolder('message', "修正 NG : タイトルまたはパスが空欄です。")
        self.embed(dict1)
        return
      sql = Text.format(UPDATE, id, title, path, artist, album, mark, info, fav, count, bindata, alindex)
      self.client.execute(sql)
      self.embed(dict1)
      self.setPlaceHolder('message', "id={0} 修正 OK".format(id))
    except Exception as e:
      self.setPlaceHolder('message', "修正 NG : " + str(e))
    return

  # データ追加
  def add(self) :
    try :
      id = ""
      title = self.getParam('title').replace("'", "''")
      path = self.getParam('path').replace("\\", "/").replace("'", "''")
      artist = MainPage.setNoneToEmpty(self.getParam('artist'))
      album = MainPage.setNoneToEmpty(self.getParam('album'))
      mark = MainPage.setNoneToEmpty(self.getParam('mark'))
      Common.log(mark)
      info = MainPage.setNoneToEmpty(self.getParam('info'))
      Common.log(info)
      fav = self.getParam('fav')
      Common.log(str(fav))
      count = self.getParam('count')
      Common.log(str(count))
      bindata = self.getParam('bindata')
      Common.log(str(bindata))
      alindex = self.getParam('alindex')
      dict1 = {'id':id, 'title':title, 'path':path, 'artist':artist, 'album':album, 'mark':mark, 'info':info, 'fav':fav, 'count':count, 'bindata':bindata, 'alindex':alindex}
      if title == "" or path == "" or title == None or path == None :
        self.setPlaceHolder('message', "追加 NG : タイトルまたはパスが空欄です。")
        self.embed(dict1)
        return
      sql = INSERT.format(title, path, artist, album, mark, info, fav, count, bindata, alindex)
      Common.log(sql)
      self.client.execute(sql)
      self.embed(dict1)
      self.setPlaceHolder('message', title + " 追加 OK")
    except Exception as e:
      self.clearAll()
      self.setPlaceHolder('message', "追加 NG : " + str(e))
    return

  # データ取得
  def query(self) :
    try :
      id = self.getParam('id')
      sql = SELECT.format(id)
      rows = self.client.query(sql)
      if len(rows) > 0 :
        row = rows[0]
        artist = MainPage.setNoneToEmpty(row[2])
        album = MainPage.setNoneToEmpty(row[3])
        mark = MainPage.setNoneToEmpty(row[4])
        info = MainPage.setNoneToEmpty(row[5])
        dict1 = {'id':id, 'title':row[0], 'path':row[1], 'artist':artist, 'album':album, 'mark':mark, 'info':info, 'fav':row[6], 'count':row[7], 'bindata':row[8], 'alindex':row[9]}
        self.embed(dict1)
        self.setPlaceHolder('message', "id={0} クエリー OK".format(id))
      else :
        self.clearAll(int(id))
        self.setPlaceHolder('message', "クエリー NG : Bad id.")
    except Exception as e :
      self.clearAll(int(id))
      self.setPlaceHolder('message', "クエリー NG : " + str(e))
    return

  # フォームのフィールドをクリアする。
  def clearAll(self, id = -1) :
    if id < 0 :
      self.setPlaceHolder('id', "")
    else :
      self.setPlaceHolder('id', id)
    dict1 = {'title':'', 'path':'', 'artist':'', 'album':'', 'mark':'', 'info':'', 'fav':0, 'count':0, 'bindata':0, 'alindex':0}
    self.embed(dict1)
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
