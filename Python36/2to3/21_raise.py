#!/usr/bin/env python3

# Python3 の raise は Python2 とは微妙に異なる。

class MyException(Exception):
 pass

try:
 raise MyException("MyException occured.")
except MyException as e:
 print(e)
