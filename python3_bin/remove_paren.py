#!/usr/bin/env python3

# ディレクトリの名前が [.+] で始まっていたら、その文字列を削除した名前にする。

from Py365Lib import Common, FileSystem as fs, Text


# START
# パラメータ確認
if Common.count_args() < 1 :
  Common.stop("Usage : remove_paren.py directory")

parent = Common.args(0)
print("cd " + parent)
dirs = fs.listDirectories(parent, True)

for d in dirs :
  parts = Text.split("/", d)
  oldname = parts[len(parts)-1]
  if Text.re_contain(r"^\[.+\].+", oldname) :
    d2 = Text.re_replace(r"\[.+\]\s", "", d)
    d2 = Text.trim(d2)
    parts = Text.split("/", d2)
    newname = parts[len(parts)-1]
    print("ren \"{0}\" \"{1}\"".format(oldname, newname))

print("echo Done.")

