#!/usr/bin/python3

#  Pictures テーブルの date 列を更新する。（最新の画像ファイルの日付にする)
#  パラメータ Pictures テーブルの id または id の範囲
from Py365Lib import Common, FileSystem as fs, MySQL
import os

mysql = MySQL.MySQL()


if Common.count_args() == 0:
  Common.stop(9, "id と日付 yyyy-mm-dd を指定してください。")
else:
  pass

id = Common.args(0)
newdate = Common.args(1)

sql = f"UPDATE Pictures SET `date`='{newdate}' WHERE id={id}"
print(sql)

mysql.execute(sql)

print("Done.")
