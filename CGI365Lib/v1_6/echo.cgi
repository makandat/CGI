#!/usr/bin/env python3
#  echo.cgi
import CGI365Lib as CGI

request = CGI.Request()
response = CGI.Response()
message = request.getParam('message')
response.sendSimple(message, "utf-8")
