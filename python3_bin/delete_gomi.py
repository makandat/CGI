#!/usr/bin/env python3
#  再帰的にゴミファイル (Thumbs.db, Desktop.ini) を削除する。
from Py365Lib import Common, FileSystem as fs
import os

# パラメータを得る。
print("== 再帰的にゴミファイル (Thumbs.db, Desktop.ini) を削除する。==")
# 対象のフォルダを得る。
if Common.count_args() == 0 :
  Common.stop(9, "フォルダを指定してください。")
folder = Common.args(0)
a = Common.readline(folder + "に対して再帰的にゴミファイルを削除します。よろしいですか？ (y/n)")
if a != "y" :
  Common.stop(1, "実行を中止しました。")

# 実行する。
files = fs.listFilesRecursively(folder, asstr=True)
i = 0
for f in files:
  f = f.replace('\\', '/')
  fn = fs.getFileName(f).lower()
  if fn == "thumbs.db" or fn == "desktop.ini" :
    print("rm -v " + f)
    os.remove(f)
    i += 1
  else :
    print("Keeped " + f)

print(f"{i} 個のファイルを削除しました。")
