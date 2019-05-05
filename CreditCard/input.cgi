#!/usr/bin/env python3
#  クレジットカード管理 データ入力
#    Version 1.01  2019-03-30 Bug fix
from WebPage import WebPage
from MySQL import MySQL
import Text


INSERT = "INSERT INTO {3}(`date`, payment, info) VALUES('{0}', {1}, '{2}')"
UPDATE = "UPDATE {0} SET "

# データ入力ページ
class InputPage(WebPage) :
  # コンストラクタ
  def __init__(self, tepmlate) :
    super().__init__(tepmlate)
    self.__mysql = MySQL()
    try :
      self.setPlaceHolder('message', "")
      if self.isParam('card') :
        self.card = "omcjcb"
        self.setPlaceHolder('card', "JCB")
        self.setPlaceHolder('back', "jcbcard.cgi")
      else :
        self.card = 'smbcvisa'
        self.setPlaceHolder('card', "VISA")
        self.setPlaceHolder('back', "index.cgi")
      b = self.isModify()
      if b == 1 :
        # 新規の場合
        self.insert()
        self.setPlaceHolder('message', "データが新規登録されました。")
      elif b == 0 :
        # 修正の場合
        if self.modify() :
          self.setPlaceHolder('message', "データが修正されました。")
        else :
          self.setPlaceHolder('message', "エラー：データが修正されませんでいた。")
      else :
        # その他の場合
        self.setPlaceHolder('message', "")
    except Exception as e:
      self.setPlaceHolder('message', Text.format("エラー {0}", str(e)))
    return


  # 新規・修正を判別する。新規=1,修正=0,その他=-1
  def isModify(self) :
    if self.isParam('submit') :
      operation = self.getParam('operation')
      return int(operation)
    else :
      return -1

  # 入力
  def insert(self) :
    global sql
    date = self.getParam('date')
    payment = Text.replace(",", "", self.getParam('payment'))
    if self.isParam('info') :
      info = self.getParam('info')
    else :
      info = ""
    sql = Text.format(INSERT, date, payment, info, self.card)
    self.__mysql.execute(sql)
    return

  # 修正
  def modify(self) :
    global sql
    sql = Text.format(UPDATE, self.card)
    comma = ""
    if self.isParam('date') :
      sql += "`date`='" + self.getParam('date') + "'"
      comma = ","
    if self.isParam('payment') :
      payment = Text.replace(",", "", self.getParam('payment'))
      sql += comma + f" payment={payment}"
      comma = ","
    if self.isParam('info') :
      info = self.getParam('info')
      sql += comma + f" info='{info}'"
    if sql == UPDATE :
      return False
    sql += Text.format(" WHERE `date`= '{0}'", self.getParam('date'))
    self.__mysql.execute(sql)
    return True


# 応答を返す。
wp = InputPage('templates/input.html')
wp.echo()
