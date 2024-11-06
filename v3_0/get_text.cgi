#!C:/Python3/python.exe
import CGI365Lib as CGI

# get_text.cgi
req, res = (CGI.Request(), CGI.Response())

path = req.getParam("path")
res.sendText(path, charset="utf-8")