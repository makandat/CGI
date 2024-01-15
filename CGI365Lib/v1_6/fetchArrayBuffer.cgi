#!/usr/bin/env python3
#  fetchArrayBuffer.cgi
import CGI365Lib as CGI

CGI.LOG = "D:/temp/fetchArrayBuffer.log"
request = CGI.Request()
response = CGI.Response()
CGI.info("fetchArrayBuffer.cgi " + request.Method)
if request.Method == "GET":
  begin = request.getParam("b")
  end = request.getParam("e")
  data = b""
  for i in range(int(begin), int(end)):
    data += b"\x0f"
elif request.Method == "POST":
  CGI.info("POST")
  data = b""
  request.parseFormBody()
  begin = request.getParam("b")
  end = request.getParam("e")
  CGI.info(begin + ", " + end)
  for i in range(int(begin), int(end)):
    data += b"\x01"
else:
  data = b"Bad REQUEST_METHOD"
response.sendBinData(data)
