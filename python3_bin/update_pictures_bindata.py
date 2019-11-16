#!/usr/bin/python3
#  指定された id の Pictures テーブルのデータの BINDATA フィールドの値を BINDATA テーブルの録された項目の id で置き換える。
from Py365Lib import MySQL, Common

if Common.count_args() == 0 :
  print("Usage: update_pictures_bindata.py Pictures_id")
  Common.stop(1)
id = Common.args(0)
mysql = MySQL.MySQL()
bindata = mysql.getValue("SELECT max(id) FROM BINDATA")
sql = f"UPDATE Pictures SET bindata={bindata} WHERE id={id}"
mysql.execute(sql)
print("Done.")
