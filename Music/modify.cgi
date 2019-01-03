#!/usr/bin/env python3
# -*- code=utf-8 -*-
# Music テーブルのデータ追加・修正
#   MySQL を利用
import WebPage as page
import FileSystem as fs
import MySQL
import Common

SELECT = "SELECT title, path, artist, album, mark, info, fav, count FROM Music WHERE id = {0}"
INSERT = "INSERT INTO Music(title, path, artist, album, mark, info, fav, count) VALUES()"
UPDATE = "UPDATE Music SET title='{1}', path='{2}', artist='{3}', album='{4}', mark='{5}', info='{6}', fav='{7}', count={8} WHERE id={0};"

# CGI WebPage クラス
class MainPage(page.WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.client = MySQL.MySQL()
    try :
      self.__mysql = MySQL.MySQL()
      if 'btnAdd' in self.params.keys() :
        if 'id' in self.params.keys() :
          self.modify()
        else :
          self.add()
      elif 'btnQuery' in self.params.keys() :
        self.query()
      else :
        self.vars['id'] = ""
        self.vars['title'] = ""
        self.vars['path'] = ""
        self.vars['artist'] = ""
        self.vars['album'] = ""
        self.vars['mark'] = ""
        self.vars['info'] = ""
        self.vars['fav'] = "0"
        self.vars['count'] = "0"
        self.vars['message'] = ""
    except Exception as e:
      self.vars['message'] = "致命的エラーを検出。" + str(e)
    return

  # データ修正
  def modify(self) :
    rb = True
    try :
      title = self.params['title'].value  if 'title' in self.params else ""
      path = self.params['path'].value  if 'path' in self.params else ""
      artist = self.params['artist'].value  if 'artist' in self.params else ""
      album = self.params['album'].value  if 'album' in self.params else ""
      mark = self.params['mark'].value  if 'mark' in self.params else ""
      info = self.params['info'].value  if 'info' in self.params else ""
      fav = self.params['fav'].value  if 'fav' in self.params else ""
      count = self.params['count'].value  if 'count' in self.params else ""
      sql = UPDATE.format(title, path, artist, album, mark, info, fav, count)
      self.client.execute(sql)
      self.vars['message'] = "修正 OK"
    except Exception as e:
      self.vars['message'] = "修正 NG : " + str(e)
    return

  # データ追加
  def add(self) :
    rb = True
    try :
      title = self.params['title'].value  if 'title' in self.params else ""
      path = self.params['path'].value  if 'path' in self.params else ""
      artist = self.params['artist'].value  if 'artist' in self.params else ""
      album = self.params['album'].value  if 'album' in self.params else ""
      mark = self.params['mark'].value  if 'mark' in self.params else ""
      info = self.params['info'].value  if 'info' in self.params else ""
      fav = self.params['fav'].value  if 'fav' in self.params else ""
      count = self.params['count'].value  if 'count' in self.params else ""
      sql = INSERT.format(title, path, artist, album, mark, info, fav, count)
      self.client.execute(sql)
      self.vars['message'] = "追加 OK"
    except Exception as e:
      self.vars['message'] = "追加 NG : " + str(e)
    return

  # データ取得
  def query(self) :
    try :
      sql = SELECT.format(self.params['id'].value)
      rows = self.client.query(sql)
      if len(rows) > 0 :
        row = rows[0]
        self.vars['id'] = self.params['id'].value
        self.vars['title'] = row[0]
        self.vars['path'] = row[1]
        self.vars['artist'] = row[2]
        self.vars['album'] = row[3]
        self.vars['mark'] = row[4]
        self.vars['info'] = row[5]
        self.vars['fav'] = row[6]
        self.vars['count'] = row[7]
        self.vars['message'] = "クエリー OK"
      else :
        self.vars['id'] = self.params['id'].value
        self.vars['title'] = ""
        self.vars['path'] = ""
        self.vars['artist'] = ""
        self.vars['album'] = ""
        self.vars['mark'] = ""
        self.vars['info'] = ""
        self.vars['fav'] = "0"
        self.vars['count'] = "0"
        self.vars['message'] = "クエリー NG : Bad id."
    except Exception as e :
      self.vars['id'] = self.params['id'].value
      self.vars['title'] = ""
      self.vars['path'] = ""
      self.vars['artist'] = ""
      self.vars['album'] = ""
      self.vars['mark'] = ""
      self.vars['info'] = ""
      self.vars['fav'] = "0"
      self.vars['count'] = "0"
      self.vars['message'] = ""
      self.vars['message'] = "クエリー NG : " + str(e)
    return

# メイン開始位置
wp = MainPage('templates/modify.html')
wp.echo()
