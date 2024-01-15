#!/usr/bin/env python3
#  fetchBLOB.cgi
import CGI365Lib as CGI

#CGI.LOG = "D:/temp/fetchBLOB.log"
request = CGI.Request()
response = CGI.Response()
if request.Method == "GET":
  begin = request.getParam("b")
  end = request.getParam("e")
  data = b""
  for i in range(int(begin), int(end)):
    data += b"\x61,"
elif request.Method == "POST":
  CGI.info("POST")
  data = b""
  request.parseFormBody()
  begin = request.getParam("b")
  end = request.getParam("e")
  CGI.info(begin + ", " + end)
  for i in range(int(begin), int(end)):
    data += b"\x51,"
else:
  data = b"Bad REQUEST_METHOD"
response.sendBinData(data)
