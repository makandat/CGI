#!/usr/bin/python3

#  Pictures テーブルの date 列を更新する。（最新の画像ファイルの日付にする)
#  パラメータ Pictures テーブルの id または id の範囲
from Py365Lib import Common, FileSystem as fs, MySQL
import os

mysql = MySQL.MySQL()


# Pictures テーブルの指定された id の date フィールドを更新する。
def updateDate(mysql, id) :
  # id から path を得る。
  path = mysql.getValue(f"SELECT path FROM Pictures WHERE id={id}")
  if path == None :
    print(f"エラー： id = {id} のデータがありません。")
    return
  print("path = ", path)

  # ディレクトリ内のファイルを検索して、一番新しいファイルの日付を得る。
  #files = fs.listFiles(path, "*", True)
  files = os.listdir(path.encode('utf-8'))
  if len(files) == 0 :
    print("エラー： ファイルが見つかりません。")
    return
  time0 = fs.getLastWrite(path + "/" + files[0].decode('utf-8'))
  pathlast = files[0].decode('utf-8')
  for f in files :
    time1 = fs.getLastWrite(path + "/" + f.decode('utf-8'))
    if time1 < time0 :
      time0 = time1
  date0 = time0[0:10]
  print(date0)

  # Pictures テーブルの当該レコードの日付(date)を更新する。
  sql = f"UPDATE Pictures SET `date`='{date0}' WHERE id={id}"
  print(sql)
  mysql.execute(sql)
  return

#  Main
# Pictures id をパラメータで指定する。
if Common.count_args() == 0 :
  Common.stop(9, "Usage: update_pictures_date.py <id of Pictures>")
else :
  pass

id0 = int(Common.args(0))
id1 = -1
if Common.count_args() > 1 :
  id1 = int(Common.args(1))
print("id0 = ", id0)
print("id1 = ", id1)

# 指定された id のレコードの日付を更新する。
if id0 > id1 :
  updateDate(mysql, id0)
else :
  for i in range(id0, id1) :
    updateDate(mysql, i)

print("Done.")

