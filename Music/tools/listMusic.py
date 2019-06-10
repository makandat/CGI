#!/usr/bin/python3
from Py365Lib import Common, FileSystem as fs
import pathlib

# 音楽拡張子一覧
AExts = ['.mp3', '.m4a', '.wma', '.flac', '.ogg', '.aac']

# Music テーブルのフィールド
MTF1 = "INSERT INTO Music VALUES(NULL,'TITLE','"
MTF2 = "','','','','', 0, 0, 0, 0);"

# パラメータチェック
if Common.count_args() == 0 :
  folder = Common.readline('検索対象のフォルダを指定してください。')
else :
  folder = Common.args(0)

# ディレクトリの存在チェック
if not fs.isDirectory(folder) :
  Common.stop(1, folder + " が見つかりません。")
else :
  print('OK')

# 再帰的にファイルを取得する。
pobj = pathlib.Path(folder)  # Generator を取得
files = pobj.glob('**/*.*')  # PosixPath のコレクション
for f in files :
  if f.is_file() and fs.getExtension(f) in AExts :
    print(MTF1 + str(f) + MTF2)

print("終わり")
