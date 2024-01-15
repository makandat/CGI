#!/usr/bin/env python3
#  postBLOB.cgi
import CGI365Lib as CGI

SAVE = "d:/temp/postBLOB.bin"
request = CGI.Request()
response = CGI.Response()
if request.Method == "POST":
  blob = request.getRawData()
  with open(SAVE, "wb") as f:
    f.write(blob)
  response.sendSimple(SAVE + " にファイル保存しました。", "utf-8")
else:
  response.sendSimple("Bad REQUEST_METHOD")