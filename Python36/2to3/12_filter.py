#!/usr/bin/env python3

# filter()グローバル関数
#  Python 2ではその戻り値としてリストを返していた。
#  しかし、Python 3ではfilter()関数はリストではなくイテレーターを返すようになっている。
def isodd(x):
 return x % 2

a = [5, 2, 4, 9, 7, 6]
it = filter(isodd, a)
for i in it:
 print(i)
