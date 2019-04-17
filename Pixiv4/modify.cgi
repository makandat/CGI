#!/usr/bin/env python3
#!C:\Program Files (x86)\Python37\python.exe
#  Pixiv Clip by Python3 v4.0  2019-04-17
#    作品お登録と修正 modify.cgi
from WebPage import WebPage
from MySQL import MySQL

# HTML ページの定義
class Pixiv4(WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.__mysql = MySQL()
    self.setPlaceHolder('message', '')
    # ポストバックか？
    if self.isParam('submit') :
      if self.isParam('id') :
        # 修正
        self.modify()
      else :
        # 挿入
        self.insert()
    elif self.isParam('query') :
      # データ確認
      self.confirm()
    else :
      # 初期状態
      self.clearAll()
    return

  # データの挿入
  def insert(self) :
    title = self.getParam('title')
    creator = self.getParam('creator')
    illust = self.getParam('illust')
    if title == "" or creator == "" or illust == "" :
      self.setPlaceHolder('message', 'エラー： 空欄の必須パラメータがあります。')
      self.setAll(('', title, creator, illust, original, tags, bindata))
      return
    original = self.getParam('original')
    tags = self.getParam('tags')
    b = self.getParam('bindata')
    bindata = 0 if b == "" else int(b)
    try :
      sql = f"INSERT INTO Pixiv3(Title,Creator,Illust_id,Original,Tags,BINDATA) VALUES('{title}','{creator}',{illust},'{original}','{tags}',{bindata})"
      self.__mysql.execute(sql)
      self.setPlaceHolder('message', title + ' を追加しました。')
      self.clearAll()
    except Exception as e :
      self.setPlaceHolder('message', 'エラー：' + str(e))
      self.setAll(('', title, creator, illust, Pixiv4.NoneToSpace(original), Pixiv4.NoneToSpace(tags), Pixiv4.NoneToSpace(bindata)))
    return

  # データの修正
  def modify(self) :
    try :
      id = self.getParam('id')
      title = self.getParam('title')
      creator = self.getParam('creator')
      illust = self.getParam('illust')
      if title == "" or creator == "" or illust == "" :
        self.setPlaceHolder('message', 'エラー： 空欄の必須パラメータがあります。')
        self.setAll((id, title, creator, illust, original, tags, bindata))
        return
      original = self.getParam('original')
      tags = self.getParam('tags')
      b = self.getParam('bindata')
      bindata = 0 if b == "" else int(b)
      sql = f"UPDATE Pixiv3 SET title='{title}', creator='{creator}', illust_id={illust}, original='{original}', tags='{tags}', bindata={bindata} WHERE id={id}"
      self.__mysql.execute(sql)
      self.setPlaceHolder('message', "id" + str(id) + ' を更新しました。')
      self.clearAll()
    except Exception as e :
      self.setPlaceHolder('message', 'エラー：' + str(e))
      self.setAll((id, title, creator, illust, Pixiv4.NoneToSpace(original), Pixiv4.NoneToSpace(tags), Pixiv4.NoneToSpace(bindata)))
    return

  # データ確認
  def confirm(self) :
    if self.isParam('id') :
      id = self.getParam('id')
      sql = f"SELECT * FROM Pixiv3 WHERE id={id}"
      rows = self.__mysql.query(sql)
      if len(rows) == 0 :
        self.setPlaceHolder('message', 'エラー：正しい id を指定してください。')
        self.clearAll()
      else :
        row = rows[0]
        self.setAll((id, row[1], row[2], row[3], Pixiv4.NoneToSpace(row[4]), Pixiv4.NoneToSpace(row[5]), Pixiv4.NoneToSpace(row[6])))
    else :
      self.setPlaceHolder('message', 'エラー：id を指定してください。')
      self.clearAll()
    return

  # 表示のクリア
  def clearAll(self) :
    self.setPlaceHolder('id', '')
    self.setPlaceHolder('title', '')
    self.setPlaceHolder('creator', '')
    self.setPlaceHolder('illust', '')
    self.setPlaceHolder('original', '')
    self.setPlaceHolder('tags', '')
    self.setPlaceHolder('bindata', '')
    return

  # 表示のセット
  def setAll(self, tup) :
    self.setPlaceHolder('id', tup[0])
    self.setPlaceHolder('title', tup[1])
    self.setPlaceHolder('creator', tup[2])
    self.setPlaceHolder('illust', tup[3])
    self.setPlaceHolder('original', tup[4])
    self.setPlaceHolder('tags', tup[5])
    self.setPlaceHolder('bindata', tup[6])
    return

  # None を "" にする。
  @staticmethod
  def NoneToSpace(x) :
    if x == None :
      return ""
    else :
      return str(x)


# プログラム開始
wp = Pixiv4('templates/modify.html')
wp.echo()