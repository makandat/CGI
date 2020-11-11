#!/usr/bin/python3
import hashlib
from Py365Lib import Common
#  md5 の計算

print("md5 の計算")
if Common.count_args() == 0 :
	instr = Common.readline('入力 > ')
else :
	instr = Common.args(0)
bstr = instr.encode()
m = hashlib.md5(bstr)
print(m.hexdigest())

