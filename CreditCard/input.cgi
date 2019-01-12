#!/usr/bin/env python3
#  クレジットカード管理 データ入力
import WebPage
import MySQL, Text


INSERT = "INSERT INTO smbcvisa(`date`, payment, info) VALUES('{0}', {1}, '{2}')"
UPDATE = "UPDATE smbcvisa SET "

class InputPage(WebPage.WebPage) :
  # コンストラクタ
  def __init__(self, tepmlate) :
    super().__init__(tepmlate)
    self.__mysql = MySQL.MySQL()
    try :
      self.vars['message'] = ""
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
    if 'submit' in self.params :
      operation = self.params['operation'].value
      return int(operation)
    else :
      return -1

  # 入力
  def insert(self) :
    global sql
    date = self.params['date'].value
    payment = Text.replace(",", "", self.params['payment'].value)
    if 'info' in self.params :
      info = self.params['info'].value
    else :
      info = ""
    sql = Text.format(INSERT, date, payment, info)
    self.__mysql.execute(sql)
    return

  # 修正
  def modify(self) :
    global sql
    sql = UPDATE
    comma = ""
    if 'date' in self.params :
      sql += "`date`='" + self.params['date'].value + "'"
      comma = ","
    if 'payment' in self.params :
      payment = Text.replace(",", "", self.params['payment'].value)
      sql += comma + f" payment={payment}"
      comma = ","
    if 'info' in self.params :
      info = self.params['info'].value
      sql += comma + f" info='{info}'"
    if sql == UPDATE :
      return False
    sql += Text.format(" WHERE `date`= '{0}'", self.params['date'].value)
    self.__mysql.execute(sql)

    return True


# 応答を返す。
wp = InputPage('templates/input.html')
wp.echo()
