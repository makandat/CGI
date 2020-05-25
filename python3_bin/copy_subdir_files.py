#!/usr/bin/env python3

# サブディレクトリ内にあるファイルを自ディレクトリに名前を変えてコピーする。
from Py365Lib import Common, FileSystem as fs, Text


# START
# パラメータ確認
if Common.count_args() < 1 :
  Common.stop("Usage : copy_subdir_files.py directory")
mydir = Common.args(0)

# サブディレクトリ一覧を得る。
dirs = fs.listDirectories(mydir, True)

# サブディレクトリごとに繰り返す。
for d in dirs :
  print(d)
  files = fs.listFiles(d, "*", True)
  parts = Text.split("/", d)
  h = parts[len(parts) - 1]
  for f in files :
    f1 = Text.replace("/", "\\", mydir + "/" + h + "/" + fs.getFileName(f))
    f2 = Text.replace("/", "\\", mydir + "/" + h + fs.getFileName(f))
    print(f"copy \"{f1}\" \"{f2}\"")

# 終わり
print("Done.")
