#!/usr/bin/env python3

# intern()グローバル関数
#   Python 3では sys.intern() になった。
#   この関数は文字列を隔離された文字列テーブルに入れる。(辞書検索のスピードがよい)
import sys

print("Python 3では sys.intern() になった。")

print(sys.intern("abc"))
