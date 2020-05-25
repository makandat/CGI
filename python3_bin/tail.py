#!/usr/bin/env python3
#  tail filePath [lines]
from Py365Lib import Common, FileSystem as fs
from collections import deque

if Common.count_args() < 1 :
  Common.stop(9, "Usage: tail filePath [lines] [encoding]")

filePath = Common.args(0)

if Common.count_args() > 1 :
  n = int(Common.args(1))
else :
  n = 20

if Common.count_args() > 2 :
  code = Common.args(2)
else :
  code = "utf-8"

fifo = deque(maxlen=n)
with open(filePath, mode="r", encoding=code) as f :
  line = f.readline()
  while line :
    fifo.append(line)
    line = f.readline()

while True :
  if len(fifo) > 0 :
    l = fifo.popleft()
    print(l, end="")
  else :
    break;
