#!/usr/bin/env python3

# リストを返す辞書メソッド
#   dictionary.keys(), items(), values() は(動的な)ビューを返すので、場合によっては不都合が起きる。

a = { "a":1, "b":2, "c":3 }

b = list(a.keys())
print(b)

b = list(a.items())
print(b)

it = iter(a.keys())
for i in it :
 print(i)

print([i for i in a.keys()])

print(min(a.keys()))
