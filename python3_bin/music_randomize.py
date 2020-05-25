#!/usr/bin/env python3
#  指定した m3u ファイルの項目（音楽ファイル) の行を入れ替えてランダム再生できるようにする。
from Py365Lib import Common, FileSystem as fs
import re
import random

if Common.count_args() == 0 :
  Common.stop(9, "m3u ファイル(UTF-8)を指定してください。")

m3u = Common.args(0)
new_m3u = m3u
if Common.count_args() >= 2 :
  new_m3u = Common.args(1)

# ファイルを読む。
lines = fs.readLines(m3u)

# 乱数の配列を作る。
randarr = []
m = len(lines)
for i in range(m) :
  n = int(random.uniform(0, 9999) + 0.5)
  randarr.append(n)

# 乱数：ファイル名の辞書を作る。
dictrand = dict()
for i in range(m) :
  dictrand[randarr[i]] = lines[i]

# dictrandをキーでソートする。
arrnew = sorted(dictrand.items())

items = []
for a in arrnew :
  items.append(a[1])

# ファイル保存
with open(new_m3u, "w", encoding="utf-8") as f  :
  f.writelines(tuple(items))


print("Done.")
