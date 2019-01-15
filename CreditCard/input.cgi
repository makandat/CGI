#!/usr/bin/env python3
#  クレジットカード管理 データ入力
import WebPage
import MySQL, Text


INSERT = "INSERT INTO {3}(`date`, payment, info) VALUES('{0}', {1}, '{2}')"
UPDATE = "UPDATE {0} SET "

# データ入力ページ
class InputPage(WebPage.WebPage) :
  # コンストラクタ
  def __init__(self, tepmlate) :
    super().__init__(tepmlate)
    self.__mysql = MySQL.MySQL()
    try :
      self.vars['message'] = ""
      if self.isParam('card') :
        self.card = "omcjcb"
        self.vars['card'] = "JCB"
        self.vars['back'] = "jcbcard.cgi"
      else :
        card = 'smbcvisa'
        self.vars['card'] = "VISA"
        self.vars['back'] = "index.cgi"
      b = self.isModify()
      if b == 1 :
        # 新規の場合
        self.insert()
        self.vars['message'] = "データが新規登録されました。"
      elif b == 0 :
        # 修正の場合
        if self.modify() :
          self.vars['message'] = "データが修正されました。"
        else :
          self.vars['message'] = "エラー：データが修正されませんでいた。"
      else :
        # その他の場合
        self.vars['message'] = ""
    except Exception as e:
      self.vars['message'] = Text.format("エラー {0} \"{1}\"", str(e), sql)
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
