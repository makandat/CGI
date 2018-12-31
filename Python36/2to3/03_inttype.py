#!/usr/bin/env python3

# Python3 では int 型が long 型と統合された。

print("int 型が long 型と統合された。")

x = 1000000000000
print(int(x))

x = 0xFFFFFFFFFFFF
print(int(x))

print(type(x) is int)

print(isinstance(x, int))
