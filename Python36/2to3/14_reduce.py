#!/usr/bin/env python3

# reduce()グローバル関数
#   reduce()関数はグローバル名前空間から取り除かれ、functoolsモジュールの中に置かれている。

from functools import reduce

print(reduce(lambda x, y: x+y, [1, 2, 3, 4, 5]))

