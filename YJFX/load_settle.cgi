#!/usr/bin/env python3
#!C:\Program Files (x86)\Python37\python.exe
#  YJFX CSV データ読み込み
#  load_settle.cgi
from WebPage import WebPage
import Text
from MySQL import MySQL

SELECT = "SELECT count(id) FROM YJFX_Settle WHERE id={0}"
INSERT = "INSERT INTO YJFX_Settle(id, CurrencyPair, Sell, price1, Date1, price2, Date2, Benefit) VALUES({0}, '{1}', '{2}', {3}, '{4}', {5}, '{6}', {7})"

# CGI WebPage クラス
class MainPage(WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.__mysql = MySQL()
    try :
      if self.isParam('data') :
        n = self.insertData()
        self.setPlaceHolder('message', str(n) + "件のデータを読み込みました。")
      else :
        self.setPlaceHolder('message', "")
    except Exception as e :
      self.setPlaceHolder('message', "クエリー NG " + str(e))
    return

  # データ読み込み
  def insertData(self) :
    lines = Text.split("\n", self.getParam('data'))
    i = 0
    # タイトル行を読み飛ばす。
    if lines[0].startswith('注文番号') :
      i = 1
    while i < len(lines) :
      line = lines[i]
      if Text.trim(line) == "" :
        break
      pline = Text.split(',', line)
      # 決済以外は無視
      if pline[0] != '決済' :
        continue
      # id (取引番号)
      id = pline[0]
      # CurrencyPair
      currency = MainPage.getCurrencyCode(pline[2])
      # Sell
      sell = '1' if pline[3] == '売' else '0'
      # price1, Date1 (取得)
      price1 = Text.replace(',', '', pline[9])
      Date1 = pline[6]
      # price2, Date2 (決済)
      price2 = Text.replace(',', '', pline[4])
      Date2 = pline[7]
      # Benefit
      benefit = Text.replace(',', '', pline[10])
      # すでに登録済みか確認
      if not self.exists(id) :
        # テーブルに挿入
        sql = Text.format(INSERT, id, currency, sell, price1, Date1, price2, Date2, benefit)
        self.__mysql.execute(sql)
      i += 1
    return i


  # Currency Pair コードを得る。
  @staticmethod
  def getCurrencyCode(jc) :
    code = "?"
    if jc == "ドル/円" :
      code = "USD/JPY"
    elif jc == "豪ドル/円" :
      code = "AUD/JPY"
    elif jc == "ユーロ/円" :
      code = "EUR/JPY"
    elif jc == "ユーロ/ドル" :
      code = "EUR/USD"
    else :
      pass
    return code

  # id が登録済みかを返す。
  def exists(self, id) :
    n = self.__mysql.getValue(Text.format(SELECT, id))
    return n > 0


# メイン開始位置
wp = MainPage('templates/load_settle.html')
wp.echo()

