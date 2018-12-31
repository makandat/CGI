#!/usr/bin/env python3

# map()グローバル関数
#   map() は Python2 ではリストを返すようになっていた。
#   Python3 ではイテレータを返す。

def cheap(x) :
 return a[x] < 150

print("map()グローバル関数")

a = { "カップヌードル":130, "赤いきつね":150, "UFO":150 }
it = map(cheap, a)
for i in it:
 print(i)
