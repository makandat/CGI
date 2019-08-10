#!/usr/bin/python3
from Py365Lib import Common, FileSystem as fs
import pathlib
import os

# 画像拡張子一覧
ImgExts = ['.jpg', '.jpeg', '.png', '.gif']

# Pictures テーブルのフィールド
PTF = "INSERT INTO Pictures VALUES(NULL, '{0}', '作者', '{1}', '', '', 0, 0, 0);"

# パラメータチェック
if Common.count_args() == 0 :
  folder = Common.readline('検索対象のフォルダを指定してください。')
else :
  folder = Common.args(0)

# ディレクトリの存在チェック
if not fs.isDirectory(folder) :
  Common.stop(1, folder + " が見つかりません。")

#print('OK')

# 再帰的に画像ファイルを含むサブフォルダ取得する。
pobj = pathlib.Path(folder)  # Generator を取得
files = pobj.glob('**/*.*')  # PosixPath のコレクション
dirset = set()
for f in files :
  if f.is_file() and fs.getExtension(f) in ImgExts :
    path = str(f).replace("\\", "/").replace("'", "''")
    dir = str(pathlib.Path(path).parent.resolve()).replace("\\", "/")
    dirset.add(dir)
    #print(dir)
for dir in dirset :
  parts = str(dir).split("/")
  n = len(parts) - 1
  title = parts[n]
  # SQL を表示 (リダイレクトを使ってファイル保存)
  print(PTF.format(title, dir))

# print("終わり")
