#!/usr/bin/env python3
# 銀行預金管理 入力・修正
import WebPage as CGI
import MySQL as DB
import Text
from syslog import syslog

INSERT = "INSERT INTO BANKS(day, bank, deposit, balance, info) VALUES('{0}', '{1}', '{2}', {3}, '{4}')"
UPDATE = "UPDATE BANKS SET {0} WHERE id={1}"


# ページクラス
class InputPage(CGI.WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.__mysql = DB.MySQL()
    self.vars['message'] = ""
    try :
      if self.isParam('id') :
        # 修正
        id = self.getParam('id')
        self.modify(id)
        self.vars['message'] = f"id {id} のデータが修正されました。"
      else :
        # 新規登録
        if self.isParam('day') :
          self.insert()
          self.vars['message'] = "データが新規登録されました。"
        else :
          self.vars['message'] = ""
    except Exception as e :
      self.vars['message'] = "エラー　" + str(e)
    return

  # 新規登録
  def insert(self) :
    day = self.getParam('day')
    bank = self.getParam('bank')
    deposit = self.getParam('deposit')
    balance = Text.replace(",", "", self.getParam('balance'))
    info = self.getParam('info')
    sql = Text.format(INSERT, day, bank, deposit, balance, info)
    syslog(sql)
    self.__mysql.execute(sql)
    return

  # データ修正
  def modify(self, id) :
    day = self.getParam('day')
    bank = self.getParam('bank')
    deposit = self.getParam('deposit')
    balance = self.getParam('balance')
    info = self.getParam('info')
    buff = ""
    comma = False
    if day != '' :
      buff += f"day='{day}'"
      comma = True
    if bank != "" :
      if comma :
        buff += f", bank='{bank}'"
      else :
        buff += f"bank='{bank}'"
        comma = True
    if deposit != "" :
      if comma :
        buff += f", deposit='{deposit}'"
      else :
        buff += f"deposit='{deposit}'"
        comma = True
    if balance != "" :
      if comma :
        buff += f", balance='{balance}'"
      else :
        buff += f"balance='{balance}'"
        comma = True
    if info != "" :
      if comma :
        buff += f", info='{info}'"
      else :
        buff += f"info='{info}'"
        comma = True
    sql = Text.format(UPDATE, buff, id)
    syslog(sql)
    self.__mysql.execute(sql)
    return



# 応答を返す。
page = InputPage('templates/input.html')
page.echo()
