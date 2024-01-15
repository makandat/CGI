#!/usr/bin/env python3
#  postBLOB2.cgi
import CGI365Lib as CGI

SAVE = "d:/temp/postBLOB2.bin"
request = CGI.Request()
response = CGI.Response()
CGI.info("postJSON.cgi " + request.Method)
if request.Method == "POST":
  blob = request.getRawString()
  with open(SAVE, "wt") as f:
    f.write(blob)
  response.sendSimple(SAVE + " にファイル保存しました。", "utf-8")
else:
  response.sendSimple("Bad REQUEST_METHOD")