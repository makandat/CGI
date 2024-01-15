#!/usr/bin/env python3
#  getJSON.cgi
import CGI365Lib as CGI

CGI.LOG = "/home/makandat/temp/getJSON.log"
request = CGI.Request()
response = CGI.Response()
CGI.info("getJSON.cgi")
a = request.getParam("a")
b = request.getParam("b")
CGI.info("a=" + a)
CGI.info("b=" + b)
response.sendJSON({"a":a, "b":b}, "utf-8")
