#!/usr/bin/env python3
#  sendJSON.cgi
import CGI365Lib as CGI
import os, sys

response = CGI.Response()
data = {"Copyright":sys.copyright, "platform":sys.platform, "OS":os.name}
response.sendJSON(data)
