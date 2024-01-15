#!/usr/bin/env python3
#  uploadTextFile.cgi
import CGI365Lib as CGI
import os

SAVE = "D:/temp/uploadTextFile.txt"
request = CGI.Request()
response = CGI.Response()
if request.Method == "POST":
  data = request.getRawData()
  if os.name == "nt":
    data = data.replace(b"\r\n", b"\n")
  with open(SAVE, "w") as f:
    text = data.decode()
    f.write(text)
  response.sendSimple(SAVE + " にファイル保存しました。", "utf-8")
else:
  response.sendSimple("Bad REQUEST_METHOD")
