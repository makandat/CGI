#!/usr/bin/python3
#  新しいサムネール画像で BINDATA テーブルを更新する。

from Py365Lib import Common, FileSystem as fs, Text, MySQL
import os, math

# 定数定義
if Common.is_windows() :
  SAVEDIR = "c:/temp/" # 注意：変更が必要
else :
  SAVEDIR = "/home/user/Pictures/Small" # 注意：変更が必要

UPDATE = "UPDATE BINDATA SET data = {0} WHERE id = {1}"

# バイナリーファイルをヘキサに変換する。
def bin2hex(filePath) :
  buff = "0x"
  b = fs.readBinary(filePath)
  buff += b.hex()
  return buff

# バイナリーファイル filePath の中身でテーブル BINDATA の id の画像データを更新する。
def updateBinaries(filePath, id) :
  filePath = filePath.replace("\\", "/")
  hexa = bin2hex(filePath)
  sql = Text.format(UPDATE, hexa, id)
  mysql_client.execute(sql)
  return



#  Start up
# パラメータ確認・取得
if Common.count_args() < 2 :
  Common.stop(1, "サムネール画像ファイルのパスと id を入力します。")
else :
  filePath = Common.args(0)
  id = Common.args(1)

# MySQL クライアントを構築
mysql_client = MySQL.MySQL()
# データ更新
updateBinaries(filePath, id)

print(f"BINDATA テーブルの id = {id} の画像データを更新しました。")
