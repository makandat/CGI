#!/usr/bin/env python3
#  postFormData.cgi
import CGI365Lib as CGI

request = CGI.Request()
response = CGI.Response()

if request.Method == "POST":
  request.parseFormBody()
  text1 = request.getParam("formText1")
  check1 = request.getParam("formCheck1")
  data  = {"formText1":text1, "formCheck1":check1}
  response.sendJSON(data, "utf-8")
else:
  response.sendJSON("Bad REQUEST_METHOD")
