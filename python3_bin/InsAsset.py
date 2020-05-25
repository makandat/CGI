#!/usr/bin/env python3

#  YJFX_Asset テーブルにデータを挿入する。
from Py365Lib import Common, MySQL

# パラメータ確認
if Common.count_args() < 3 :
  Common.stop(9, "Usage: InsAsset.py date asset loss", Common.ESC_FG_YELLOW)

date = Common.args(0)
asset = Common.args(1)
loss = Common.args(2)

sql = f"INSERT INTO YJFX_Asset VALUES(null, '{date}', {asset}, {loss}, '')"

mysql = MySQL.MySQL()
mysql.execute(sql)

sql = "SELECT * FROM VW_YJFX_Asset"
result = mysql.query(sql)

for row in result :
  print(row)

print("Done.")
