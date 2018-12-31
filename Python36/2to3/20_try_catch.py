#!/usr/bin/env python3

# Python3 の try catch は Python2 とは微妙に異なる。

try:
 import mymodule
except ImportError as e:
 print(e)
