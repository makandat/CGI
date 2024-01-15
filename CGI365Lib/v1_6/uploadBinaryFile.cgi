#!/usr/bin/env python3
#  uploadBinaryFile.cgi
import CGI365Lib as CGI

SAVE = "D:/temp/uploadBinaryFile.bin"
request = CGI.Request()
response = CGI.Response()
if request.Method == "POST":
  data = request.getRawData()
  with open(SAVE, "wb") as f:
    f.write(data)
  response.sendSimple(SAVE + " にファイル保存しました。", "utf-8")
else:
  response.sendSimple("Bad REQUEST_METHOD")
