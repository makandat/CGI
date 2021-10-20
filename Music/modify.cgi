#!C:\python3\python.exe
#!/usr/bin/env python3
# -*- code=utf-8 -*-
# Music テーブルのデータ追加・修正 (modify.cgi)
#   MySQL を利用
from WebPage import WebPage
import FileSystem as fs
from MySQL import MySQL
import Common
import Text
#from syslog import syslog

SELECT = "SELECT album, title, path, artist, media, mark, info, fav, count, bindata, DATE_FORMAT(`date`, '%Y-%m-%d') FROM Music WHERE id = {0}"
INSERT = "INSERT INTO Music(album, title, path, artist, media, mark, info, fav, count, bindata, `date`) VALUES({0}, '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', {7}, {8}, {9}, CURRENT_DATE())"
UPDATE = "UPDATE Music SET album={1}, title='{2}', path='{3}', artist='{4}', media='{5}', mark='{6}', info='{7}', fav={8}, count={9}, bindata={10} WHERE id={0};"

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
      album = MainPage.setNoneToEmpty(self.getParam('album'))
      title = Text.replace("'", "''", self.getParam('title'))
      path = Text.replace("'", "''", self.getParam('path').replace("\\", "/"))
      artist = MainPage.setNoneToEmpty(self.getParam('artist'))
      media = MainPage.setNoneToEmpty(self.getParam('media'))
      mark = MainPage.setNoneToEmpty(self.getParam('mark'))
      info = MainPage.setNoneToEmpty(self.getParam('info'))
      fav = self.getParam('fav', 0)
      count = self.getParam('count', 0)
      bindata = self.getParam('bindata', 0)
      dict1 = {'id':id, 'album':album, 'title':title, 'path':path, 'artist':artist, 'media':media, 'mark':mark, 'info':info, 'fav':fav, 'count':count, 'bindata':bindata}
      if title == "" or path == "" or title == None or path == None :
        self.setPlaceHolder('message', "修正 NG : タイトルまたはパスが空欄です。")
        self.embed(dict1)
        return
      sql = Text.format(UPDATE, id, album, title, path, artist, media, mark, info, fav, count, bindata)
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
      album = MainPage.setNoneToEmpty(self.getParam('album'))
      title = self.getParam('title').replace("'", "''")
      path = self.getParam('path').replace("\\", "/").replace("'", "''")
      artist = MainPage.setNoneToEmpty(self.getParam('artist'))
      mark = MainPage.setNoneToEmpty(self.getParam('mark'))
      #Common.log(mark)
      info = MainPage.setNoneToEmpty(self.getParam('info'))
      #Common.log(info)
      fav = self.getParam('fav')
      #Common.log(str(fav))
      count = self.getParam('count')
      #Common.log(str(count))
      bindata = self.getParam('bindata')
      #Common.log(str(bindata))
      dict1 = {'id':id, 'album':album, 'title':title, 'path':path, 'artist':artist, 'mark':mark, 'info':info, 'fav':fav, 'count':count, 'bindata':bindata}
      if title == "" or path == "" or title == None or path == None :
        self.setPlaceHolder('message', "追加 NG : タイトルまたはパスが空欄です。")
        self.embed(dict1)
        return
      sql = INSERT.format(album, title, path, artist, mark, info, fav, count, bindata)
      #Common.log(sql)
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
        album = row[0]
        title = row[1]
        path = row[2]
        artist = MainPage.setNoneToEmpty(row[3])
        media = MainPage.setNoneToEmpty(row[4])
        mark = MainPage.setNoneToEmpty(row[5])
        info = MainPage.setNoneToEmpty(row[6])
        fav = row[7]

        dict1 = {'id':id, 'album':album, 'title':title, 'path':path, 'media':media, 'artist':artist, 'mark':mark, 'info':info, 'fav':fav, 'count':row[8], 'bindata':row[9]}
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
    dict1 = {'album':0, 'title':'', 'path':'', 'artist':'', 'media':'', 'mark':'', 'info':'', 'fav':0, 'count':0, 'bindata':0}
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
