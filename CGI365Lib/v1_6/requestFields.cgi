#!/usr/bin/env python3
#  requestFields.cgi
import os
import CGI365Lib as CGI

def dictToString(data):
  s = "{"
  for k, v in data.items():
    s += f"{k}:{v},"
  return s + "}"

request = CGI.Request()
response = CGI.Response()

map = dict()
map["RawData"] = request.RawData.decode()
map["QueryString"] = request.QueryString
map["Method"] = request.Method
map["Address"] = dictToString(request.Address)
map["Cookie"] = dictToString(request.Cookie)
map["Query"] = dictToString(request.Query)
map["Form"] = dictToString(request.Form)
map["PathInfo"] = request.PathInfo

response.sendJSON(map, "utf-8")
