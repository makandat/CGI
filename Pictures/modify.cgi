#!/usr/bin/env python3
# -*- code=utf-8 -*-
# Pictures テーブルのデータ追加・修正
#   MySQL を利用
import WebPage as page
import FileSystem as fs
import MySQL
import Common
import Text
from syslog import syslog

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
      if 'btnAdd' in self.params.keys() :
        # 追加・修正ボタンのとき
        if 'id' in self.params.keys() :
          # id が指定されている場合
          self.modify()
        else :
          # id が指定されていない場合
          self.add()
      elif 'btnQuery' in self.params.keys() :
        # データ確認ボタンの時
        self.query()
      else :
        # その他の場合
        self.clearAll()
        self.vars['message'] = ""
    except Exception as e:
      self.vars['message'] = "致命的エラーを検出。" + str(e)
    return

  # データ修正
  def modify(self) :
    rb = True
    try :
      id = self.params['id'].value
      title = Text.replace("'", "''", self.params['title'].value)  if 'title' in self.params else ""
      path = Text.replace("'", "''", self.params['path'].value)  if 'path' in self.params else ""
      if title == "" or path == "" or title == None or path == None :
        self.vars['message'] = "修正 NG : タイトルまたはパスが空欄です。"
        self.vars['id'] = ""
        self.vars['title'] = title
        self.vars['path'] = path
        self.vars['artist'] = MainPage.setNoneToEmpty(artist)
        self.vars['album'] = MainPage.setNoneToEmpty(album)
        self.vars['mark'] = MainPage.setNoneToEmpty(mark)
        self.vars['info'] = MainPage.setNoneToEmpty(info)
        self.vars['fav'] = fav
        self.vars['count'] = str(count)
        return
      artist = MainPage.setNoneToEmpty(self.params['artist'].value  if 'artist' in self.params else "")
      album = MainPage.setNoneToEmpty(self.params['album'].value  if 'album' in self.params else "")
      mark = MainPage.setNoneToEmpty(self.params['mark'].value  if 'mark' in self.params else "")
      info = MainPage.setNoneToEmpty(self.params['info'].value  if 'info' in self.params else "")
      fav = self.params['fav'].value  if 'fav' in self.params else ""
      count = self.params['count'].value  if 'count' in self.params else ""
      sql = Text.format(UPDATE, id, title, path, artist, album, mark, info, fav, count)
      self.client.execute(sql)
      self.vars['id'] = id
      self.vars['title'] = title
      self.vars['path'] = path
      self.vars['artist'] = artist
      self.vars['album'] = album
      self.vars['mark'] = mark
      self.vars['info'] = info
      self.vars['fav'] = fav
      self.vars['count'] = str(count)
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
      if title == "" or path == "" or title == None or path == None :
        self.vars['message'] = "追加 NG : タイトルまたはパスが空欄です。"
        self.vars['id'] = ""
        self.vars['title'] = title
        self.vars['path'] = path
        self.vars['artist'] = MainPage.setNoneToEmpty(artist)
        self.vars['album'] = MainPage.setNoneToEmpty(album)
        self.vars['mark'] = MainPage.setNoneToEmpty(mark)
        self.vars['info'] = MainPage.setNoneToEmpty(info)
        self.vars['fav'] = fav
        self.vars['count'] = str(count)
        return
      artist = MainPage.setNoneToEmpty(self.params['artist'].value  if 'artist' in self.params else "")
      album = MainPage.setNoneToEmpty(self.params['album'].value  if 'album' in self.params else "")
      mark = MainPage.setNoneToEmpty(self.params['mark'].value  if 'mark' in self.params else "")
      info = MainPage.setNoneToEmpty(self.params['info'].value  if 'info' in self.params else "")
      fav = self.params['fav'].value  if 'fav' in self.params else ""
      count = self.params['count'].value  if 'count' in self.params else ""
      sql = INSERT.format(title, path, artist, album, mark, info, fav, count)
      self.client.execute(sql)
      self.vars['id'] = ""
      self.vars['title'] = title
      self.vars['path'] = path
      self.vars['artist'] = MainPage.setNoneToEmpty(artist)
      self.vars['album'] = MainPage.setNoneToEmpty(album)
      self.vars['mark'] = MainPage.setNoneToEmpty(mark)
      self.vars['info'] = MainPage.setNoneToEmpty(info)
      self.vars['fav'] = fav
      self.vars['count'] = str(count)
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
        self.vars['artist'] = MainPage.setNoneToEmpty(row[2])
        self.vars['album'] = MainPage.setNoneToEmpty(row[3])
        self.vars['mark'] = MainPage.setNoneToEmpty(row[4])
        self.vars['info'] = MainPage.setNoneToEmpty(row[5])
        self.vars['fav'] = row[6]
        self.vars['count'] = row[7]
        self.vars['message'] = "クエリー OK"
      else :
        self.clearAll(int(self.params['id'].value))
        self.vars['message'] = "クエリー NG : Bad id."
    except Exception as e :
      self.clearAll(int(self.params['id'].value))
      self.vars['message'] = "クエリー NG : " + str(e)
    return

  # フォームのフィールドをクリアする。
  def clearAll(self, id = -1) :
    if id < 0 :
      self.vars['id'] = ""
    else :
      self.vars['id'] = str(id)
    self.vars['title'] = ""
    self.vars['path'] = ""
    self.vars['artist'] = ""
    self.vars['album'] = ""
    self.vars['mark'] = ""
    self.vars['info'] = ""
    self.vars['fav'] = "0"
    self.vars['count'] = "0"
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
