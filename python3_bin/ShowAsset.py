#!/usr/bin/env python3

#  YJFX_Asset テーブルにデータを挿入する。
from Py365Lib import Common, MySQL, Text


mysql = MySQL.MySQL()

sql = "SELECT * FROM VW_YJFX_Asset"
result = mysql.query(sql)

print("ID       Date            Asset         ProfitLoss")
for row in result :
  print("{0}\t{1}\t{2}\t{3}".format(row[0], row[1], Text.money(row[2]), Text.money(row[3])))

print("Done.")
