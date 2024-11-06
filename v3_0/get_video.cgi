#!C:/Python3/python.exe
import CGI365Lib as CGI

req, res = (CGI.Request(), CGI.Response())

path = req.getParam("path")
res.sendVideo(path)