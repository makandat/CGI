#!/usr/bin/env python3
# Videos テーブルにビデオファイル一覧を挿入する。
#   python3 InsVideos.py path {'print'/'insert'}
from Py365Lib import Common, FileSystem, MySQL, Text
import glob

VIDEOEXT = ['.mp4', '.avi', '.mkv', '.mov', '.mpg']
PWD = 'ust62kjy'
UID = 'user'

# ビデオファイル一覧を取得
def getVideoFiles(path) :
  files = glob.glob(path + "/**/*", recursive=True)
  vfiles = list()
  for f in files :
    ext = FileSystem.getExtension(f)
    if ext in VIDEOEXT :
      fn = str(f).replace("\\", "/")
      vfiles.append(str(fn))
  return vfiles

# Main Program
def main() :
  print("** Videos テーブル用ビデオファイル一覧を作成または挿入する。**")
  # path 取得
  if Common.count_args() == 0 :
    Common.stop(1, "使用方法: python3 InsVideos.py path insert")
  path = Common.args(0)
  # print/insert オプション取得
  insoption = False
  if Common.count_args() == 2 :
    insoption = True
  # 確認
  if not insoption :
    print(f"Path = {path}, Videos テーブルに挿入 = {insoption}")
    a = Common.readline("Confirm (Y/N) > ")
    if Text.tolower(a) != 'y' :
      Common.stop(2, "実行を中止しました。")
  else :
    pass
  # ビデオファイル一覧を取得する。
  vfiles = getVideoFiles(path)
  # INSERT 文を作成する。
  sql = "INSERT INTO Videos VALUES"
  for p in vfiles :
    p = p.replace("'", "''")
    fileName = FileSystem.getFileName(p)
    title = Text.left(fileName, len(fileName) - 4)
    sql += f"(NULL, '0', '{title}', '{p}', '', '', '', '', 0, 0, 0, 0, 0),\n"
    print(p)
  sql = Text.left(sql, len(sql) - 2) + ";"
  if not insoption :
    print(sql)
  if insoption :
    # INSERT 文を実行する。
    try :
      mysql = MySQL.MySQL(UID, PWD, UID)
      mysql.execute(sql)
      # 終了メッセージ
      if not insoption :
        print("正常に終了しました。")
    except Error as e:
      Common.stop("MySQL のエラーにより終了。接続条件やSQL をチェックしてください。" + e.message)
  return

# START UP
main()
