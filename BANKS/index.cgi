#!/usr/bin/env python3
# 銀行預金管理
import WebPage as CGI
import MySQL as DB
import Text
from syslog import syslog

SELECT = "SELECT id, day, bank, deposit, balance, info FROM BANKS"



# ページクラス
class IndexPage(CGI.WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.__mysql = DB.MySQL()
    self.vars['message'] = ""
    try :
      # 銀行コードを得る。
      bank = ""
      if 'bank' in self.params :
        bank = self.params['bank'].value
      rawspan = ""
      # 期間を得る。
      if 'span' in self.params :
        rawspan = self.params['span'].value
      # クエリー結果を得る。
      self.vars['content'] = self.getContent(bank, rawspan)
    except Exception as e:
      self.vars['message'] = "エラー " + str(e)
    return

  # ページ内容を作成する。
  def getContent(self, bank, rawspan) :
    # SQL を構築する。
    buff = ""
    # すべての銀行の場合
    if bank == "0000" :
      bank = ""
    # パラメータなしの場合
    if len(bank) == 0 and len(rawspan) == 0 :
      sql = SELECT
    else :
      sql = SELECT + " WHERE "
      #⃣bank のみが有効
      if len(bank) > 0 and len(rawspan) == 0 :
        sql += Text.format(" bank='{0}'", bank)
      # rawspan のみが有効
      elif len(bank) == 0 and len(rawspan) > 0 :
        span = Text.split('-', rawspan)
        span0 = IndexPage.convert_month(span[0], '01')
        span1 = IndexPage.convert_month(span[1], '31')
        sql += Text.format(" day BETWEEN '{0}' AND '{1}'", span0, span1)
      # どちらも有効
      elif len(bank) > 0 and len(rawspan) > 0 :
        span = Text.split('-', rawspan)
        span0 = IndexPage.convert_month(span[0], '01')
        span1 = IndexPage.convert_month(span[1], '31')
        sql += Text.format(" day BETWEEN '{0}' AND '{1}'", span0, span1)
        sql += Text.format(" AND bank='{0}'", bank)
    # クエリーを行う。
    rows = self.__mysql.query(sql)
    # HTML に変換する。
    row2 = [0, '', '',  '', 0, '']
    for row in rows :
      row2[0] = row[0]
      row2[1] = row[1]
      row2[2] = IndexPage.get_bank(row[2])
      n = int(row[3])
      row2[3] = '外貨' if n == 1 else '普通'
      row2[4] = Text.money(row[4])
      row2[5] = "" if row[5] == None else row[5]
      s = CGI.WebPage.table_row(row2)
      buff += s + "\n"
    return buff


  # 銀行名を得る。
  @staticmethod
  def get_bank(code:str) -> str :
    name = ""
    if code == "0009" :
      name = "三井住友銀行"
    elif code == "0133" :
      name = "武蔵野銀行"
    elif code == "0038" :
      name = "住信SBIネット銀行"
    else :
      name = str(code)
    return name

  # yymm を 20yy-mm-last に変換する。
  @staticmethod
  def convert_month(month, last) :
    str1 = Text.Text(month)
    s0 = str1.left(2)
    s1 = str1.right(2)
    month = "20" + s0 + "-" + s1 + "-" + last
    return month

# 応答を返す。
page = IndexPage('templates/index.html')
page.echo()
