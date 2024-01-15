#!/usr/bin/env python3
#  postFormData2.cgi
import CGI365Lib as CGI

SAVE = "d:/temp/postFormData2.txt"
request = CGI.Request()
response = CGI.Response()
if request.Method == "POST":
  request.parseFormBody()
  text2 = request.getParam("formText2")
  filename = request.getParam("filename-formFile2")
  file2 = request.getParam("chunk-formFile2")
  with open(SAVE, "wb") as f:
    f.write(file2)
  data  = {"formText2":text2, "filename":filename}
  response.sendJSON(data, "utf-8")
else:
  response.sendJSON("Bad REQUEST_METHOD")
