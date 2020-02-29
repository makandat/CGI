#!/usr/bin/env python3
#!C:\Program Files (x86)\Python37\python.exe
#!C:\Program Files\Python3\python.exe
# -*- code=utf-8 -*-
#   modify_album.cgi  Version 1.25
from WebPage import WebPage
from MySQL import MySQL
import FileSystem as fs
import Common
#from syslog import syslog

LIMIT = 200

# CGI WebPage クラス
class MainPage(WebPage) :

  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.__mysql = MySQL()
    self.setPlaceHolder('title', 'アルバムの作成と修正')
    self.setPlaceHolder('message', '')
    if self.isParam('submit') :
      id = self.getParam('id')
      if id == "" :
        self.insert()
      else :
        self.modify(id)
    elif self.isParam('query') :
      if self.isParam('id') :
        id = self.getParam('id')
        try:
          self.query(id)
        except :
          self.setPlaceHolder('message', 'エラー： 致命的なエラーを検出。')
          self.clear()
      else :
        self.setPlaceHolder('message', 'エラー： id が空欄です。')
        self.clear()
    else :
      self.clear()
    return

  # コントロールの値をクリア
  def clear(self) :
    self.setPlaceHolder('id', '')
    self.setPlaceHolder('name', '')
    self.setPlaceHolder('picture', 'selected')
    self.setPlaceHolder('music', '')
    self.setPlaceHolder('video', '')
    self.setPlaceHolder('other', '')
    self.setPlaceHolder('info', '')
    self.setPlaceHolder('bindata', '0')
    self.setPlaceHolder('groupname', '')
    return

  def setValues(self) :
    self.setPlaceHolder('id', self.getParam('id'))
    self.setPlaceHolder('name', self.getParam('name'))
    selected = self.getParam('mark')
    self.setPlaceHolder('picture', '')
    self.setPlaceHolder('music', '')
    self.setPlaceHolder('video', '')
    self.setPlaceHolder('other', '')
    self.setPlaceHolder(selected, 'selected')
    self.setPlaceHolder('info', self.getParam('info'))
    if self.isParam('bindata') :
      bindata = self.getParam('bindata')
    else :
      bindata = '0'
    if self.isParam('groupname') :
      groupname = self.getParam('groupname')
    else :
      groupname = ''
    self.setPlaceHolder('groupname', groupname)
    return

  # データ挿入
  def insert(self) :
    name = self.getParam('name')
    if name == '' :
      self.setPlaceHolder('message', 'アルバム名が空欄です。')
      self.setValues()
      return
    mark = self.getParam('mark')
    info = self.getParam('info')
    bindata = self.getParam('bindata')
    if bindata == '' :
      bindata = 0
    groupname = self.getParam('groupname')
    sql = f"INSERT INTO Album(name, mark, info, bindata, groupname) VALUES('{name}', '{mark}', '{info}', {bindata}, '{groupname}')"
    try :
      self.__mysql.execute(sql)
      self.setPlaceHolder('message', f"{name} が挿入されました。")
      self.clear()
    except Exception as e :
      self.setPlaceHolder('message', str(e))
      self.setValues()
    return

  # データ更新
  def modify(self, id) :
    name = self.getParam('name')
    if name == '' :
      self.setPlaceHolder('message', 'アルバム名が空欄です。')
      self.setValues()
      return
    mark = self.getParam('mark')
    info = self.getParam('info')
    bindata = self.getParam('bindata')
    if bindata == '' :
      bindata = 0
    groupname = self.getParam('groupname')
    sql = f"UPDATE Album SET name='{name}', mark='{mark}', info='{info}', bindata={bindata}, groupname='{groupname}' WHERE id={id}"
    try :
      self.__mysql.execute(sql)
      self.setPlaceHolder('message', f"{name} が修正されました。")
      self.clear()
    except Exception as e :
      self.setPlaceHolder('message', str(e))
      self.setValues()
    return

  # データ確認
  def query(self, id) :
    sql = f"SELECT id, name, mark, info, bindata, groupname FROM Album WHERE id={id}"
    rows = self.__mysql.query(sql)
    if len(rows) == 0 :
      self.setPlaceHolder('message', 'データがありません。正しい id を入力してください。')
      self.clear()
    else :
      row = rows[0]
      self.setPlaceHolder('message', 'id に対応するデータが見つかりました。')
      self.setPlaceHolder('id', id)
      self.setPlaceHolder('name', row[1])
      self.setPlaceHolder('mark', row[2])
      self.setPlaceHolder('info', row[3])
      self.setPlaceHolder('bindata', row[4])
      if row[5] == None :
        groupname = ""
      else :
        groupname = row[5]
      self.setPlaceHolder('groupname', groupname)
    return
    
# 実行開始
wp = MainPage('templates/modify_album.html')
wp.echo()
