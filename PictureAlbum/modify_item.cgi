#!/usr/bin/env python3
#!C:\Program Files (x86)\Python37\python.exe
# -*- code=utf-8 -*-
#   modify_album.cgi  Version 1.00
from WebPage import WebPage
from MySQL import MySQL
import FileSystem as fs
import Text
import Common
#from syslog import syslog

LIMIT = 200

# CGI WebPage クラス
class MainPage(WebPage) :

  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    #Common.init_logger('/var/www/data/Loggrt.log')
    self.__mysql = MySQL()
    self.setPlaceHolder('message', '')
    if self.isParam('submit') :
      if self.isParam('id') :
        self.modify()
      else :
        self.insert()
    elif self.isParam('query') :
      if self.isParam('id') :
        try:
          self.query()
        except:
          self.setPlaceHolder('message', 'エラー： 致命的なエラーを検出。')
          self.clear()
      else :
        self.setPlaceHolder('message', 'エラー： id が空欄です。')
        self.clear()
    else :
      self.clear()
    return

  # フォームのコントロールをクリアする。
  def clear(self) :
    self.setPlaceHolder('id', '')
    self.setPlaceHolder('album', '')
    self.setPlaceHolder('title', '')
    self.setPlaceHolder('path', '')
    self.setPlaceHolder('creator', '')
    self.setPlaceHolder('info', '')
    self.setPlaceHolder('fav', '0')
    self.setPlaceHolder('bindata', '0')
    return

  # フォームのコントロールをパラメータで値を設定する。
  def setValues(self, id=0) :
    if id == 0 :
      self.setPlaceHolder('id', self.getParam('id'))
    else :
      self.setPlaceHolder('id', str(id))
    self.setPlaceHolder('album', self.getParam('album'))
    self.setPlaceHolder('title', self.getParam('title'))
    self.setPlaceHolder('path', self.getParam('path'))
    self.setPlaceHolder('creator', self.getParam('creator'))
    self.setPlaceHolder('info', self.getParam('info'))
    if self.isParam('fav') :
      fav = self.getParam('fav')
    else :
      fav = '0'
    self.setPlaceHolder('fav', fav)
    if self.isParam('bindata') :
      bindata = self.getParam('bindata')
    else :
      bindata = '0'
    self.setPlaceHolder('bindata', bindata)
    return

  # データ挿入
  def insert(self) :
    album = ""
    if self.isParam('album') :
      album = self.getParam('album')
    else :
      self.setPlaceHolder('message', 'アルバム番号が空欄です。')
      self.setValues()
      return
    title = ""
    if self.isParam('title') :
      title = self.getParam('title')
      title = Text.replace("'", "''", title)
    else :
      self.setPlaceHolder('message', 'タイトルが空欄です。')
      self.setValues()
      return
    path = ""
    if self.isParam('path') :
      path = self.getParam('path')
      path = Text.replace("\\", "/", path)
      path = Text.replace("'", "''", path)
    else :
      self.setPlaceHolder('message', 'パスが空欄です。')
      self.setValues()
      return
    creator = ""
    if self.isParam('creator') :
      creator = self.getParam('creator')
    else :
      self.setPlaceHolder('message', '作者が空欄です。')
      self.setValues()
      return
    info = self.getParam('info')
    fav = self.getParam('fav')
    if fav == '' :
      fav = 0
    bindata = self.getParam('bindata')
    if bindata == '' :
      bindata = 0
    sql = f"INSERT INTO PictureAlbum(album,title,path,creator,info,fav,bindata) VALUES('{album}','{title}','{path}','{creator}','{info}', {fav}, {bindata})"
    try :
      self.__mysql.execute(sql)
      self.setPlaceHolder('message', f"{title} をテーブル PictureAlbum に挿入しました。")
    except Exception as e :
      self.setPlaceHolder('message', str(e))
    self.setValues()
    return

  # データ修正
  def modify(self) :
    id = self.getParam('id')
    album = ""
    if self.isParam('album') :
      album = self.getParam('album')
    else :
      self.setPlaceHolder('message', 'アルバム番号が空欄です。')
      self.setValues()
      return
    title = ""
    if self.isParam('title') :
      title = self.getParam('title')
      title = Text.replace("'", "''", title)
    else :
      self.setPlaceHolder('message', 'タイトルが空欄です。')
      self.setValues()
      return
    path = ""
    if self.isParam('path') :
      path = self.getParam('path')
      path = Text.replace("\\", "/", path)
      path = Text.replace("'", "''", path)
    else :
      self.setPlaceHolder('message', 'パスが空欄です。')
      self.setValues()
      return
    creator = ""
    if self.isParam('creator') :
      creator = self.getParam('creator')
    else :
      self.setPlaceHolder('message', '作者が空欄です。')
      self.setValues()
      return
    info = self.getParam('info')
    fav = self.getParam('fav')
    if fav == '' :
      fav = 0
    bindata = self.getParam('bindata')
    if bindata == '' :
      bindata = 0
    sql = f"UPDATE PictureAlbum SET album='{album}', title='{title}', path='{path}', creator='{creator}', info='{info}', fav={fav}, bindata={bindata} WHERE id={id}"
    try :
      self.__mysql.execute(sql)
      self.setPlaceHolder('message', f"id={id} のデータを更新しました。")
    except Exception as e :
      self.setPlaceHolder('message', str(e))
    self.setValues(id)

  # データ確認
  def query(self) :
    if not self.isParam('id') :
      self.setPlaceHolder('message', 'id が指定されていません。')
      self.clear()
      return
    id = self.getParam('id')
    sql = f"SELECT album,title,path,creator,info,fav,bindata FROM PictureAlbum WHERE id={id}"
    rows = self.__mysql.query(sql)
    if len(rows) == 0 :
      self.setPlaceHolder('message', 'id が正しくありません。データがありません。')
      self.clear()
      return
    row = rows[0]
    self.setPlaceHolder('id', id)
    self.setPlaceHolder('album', row[0])
    self.setPlaceHolder('title', row[1])
    self.setPlaceHolder('path', row[2])
    self.setPlaceHolder('creator', row[3])
    self.setPlaceHolder('info', row[4])
    self.setPlaceHolder('fav', row[5])
    self.setPlaceHolder('bindata', row[6])
    return

# 実行開始
wp = MainPage('templates/modify_item.html')
wp.echo()
