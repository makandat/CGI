#!/usr/bin/env python3
#  Pictures テーブルの PATH フィールドを解析して creator を更新する。
from Py365Lib import Common, MySQL as mysql, Text

# Pictures テーブルの PATH フィールドを解析して creator を更新する関数
def doChangeCreator() :
  sql = Text.format("SELECT id, creator, path FROM Pictures WHERE id BETWEEN {0} AND {1}", id_start, id_end)
  Common.esc_print("cyan", sql)
  UPDATE = "UPDATE Pictures SET creator='{0}' WHERE id={1}"
  client = mysql.MySQL()
  rows = client.query(sql)
  for row in rows :
    id = row[0]
    creator = row[1]
    path = row[2]
    if creator == "作者" :
      ppath = Text.split('/', path)
      lenpath = len(ppath)
      new_creator = ppath[lenpath - 2]
      sql = Text.format(UPDATE, new_creator, id)
      print(sql)
      client.execute(sql)
      print(sql)
    else:
      pass
  return


#
#  メイン
# ID の範囲を決める。
id_start = 1
id_end = 1000000
id_range = Common.readline("id の範囲 (nnnn-nnnn) を入力してください。(省略時はすべて)")
if id_range == "" :
  Common.esc_print("yellow", "すべての id に対して実行します。(y/n)")
  a = Common.readline(">")
  if y != "y" :
    Common.stop(9, "実行を中止しました。")
else :
  nn = Text.split('-', id_range)
  if len(nn) == 2 :
    id_start = int(nn[0])
    id_end = int(nn[1])
  else :
    Common.stop(9, "範囲が正しくありません。実行を中止しました。")
  # Pictures テーブルからクエリーを行って対象のデータを得る。
  doChangeCreator()
  print("完了")
