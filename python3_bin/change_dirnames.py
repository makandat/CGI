#!/usr/bin/env python3

# ディレクトリに ^\[.+\]$ が含まれる場合、\[,\] を取る。
# サブディレクトリが ^\[.+\] .+ なら \[.+\] を取る。

from Py365Lib import Common, FileSystem as fs, Text


# START
# パラメータ確認
if Common.count_args() < 1 :
  Common.stop("Usage : change_dirnames.py directory")

# ディレクトリ一覧を得る。
parent = Common.args(0)
dirs = fs.listDirectories(parent, True)

# ディレクトリ名 [.+] を見つける。
for d in dirs :
  if Text.re_contain(r".+\[.+\]$", d) :
    d2 = Text.replace("[", "", d)
    d2 = Text.replace("]", "", d2)
    fs.move(d, d2)
    print(d2)
print("**************")
# サブディレクトリに ^\[.+\] .+ を見つける。
dirs = fs.listDirectories(parent, True)
for d in dirs :
  dirs2 = fs.listDirectories(d, True)
  for d2 in dirs2 :
    d3 = Text.re_replace(r"\[.+\]\s+", "", d2)
    fs.move(d2, d3)
    print(d3)

# 終わり
print("Done.")
