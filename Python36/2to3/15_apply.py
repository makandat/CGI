#!/usr/bin/env python3

# apply()グローバル関数
#   Python 3ではapply()関数は廃止されている。

def func(a, b, c):
 return a + b + c

print("Python 3ではapply()関数は廃止されている。")

# 代わりに可変長引数で渡す。
a = [1, 2, 3]
print(func(*a))
