#!/usr/bin/env python3

# next()イテレータメソッド --> next()というグローバル関数

a = [ 'a', 'b', 'c', 'd' ]
it = iter(a)

try:
 while True:
  y = next(it)
  print(y)
except:
 pass
