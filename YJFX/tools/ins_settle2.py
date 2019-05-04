#!/usr/bin/python3
#  YJFX 決済CSVデータ読み込み  ins_settle2.py
import Common
import Text
import FileSystem as fs
from MySQL import MySQL

SELECT = "SELECT count(id) FROM YJFX_Settle WHERE id={0}"
INSERT = "INSERT INTO YJFX_Settle(id, CurrencyPair, Sell, price1, Date1, price2, Date2, Benefit) VALUES({0}, '{1}', '{2}', {3}, '{4}', {5}, '{6}', {7})"


# MySQL オブジェクト
mysql = None

# id が登録済みかを返す。
def id_exists(id) :
  n = mysql.getValue(Text.format(SELECT, id))
  return n > 0

# Currency Pair コードを得る。
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

# データ読み込み
def insertData(data) :
  lines = Text.split("\n", data)
  # タイトル行を読み飛ばす。
  i = 1
  while i < len(lines) :
    line = lines[i]
    if Text.trim(line) == "" :
      break
    pline = Text.split(',', line)
    # id (取引番号)
    id = pline[0]
    # CurrencyPair
    print("pline[2]=" + str(pline[2]))
    currency = getCurrencyCode(pline[2])
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
    if not id_exists(id) :
      # テーブルに挿入
      sql = Text.format(INSERT, id, currency, sell, price1, Date1, price2, Date2, benefit)
      mysql.execute(sql)
    i += 1
  return i



# Main
# 決済CSVファイル読み込み
if Common.count_args() == 0 :
  Common.stop(1, "CSV ファイルを指定してください。")

mysql = MySQL()

filePath = Common.args(0)
data = fs.readAllText(filePath)
n = insertData(data)
print(f"{n} 行読み込みました。")

