#!D:/python312/python.exe
import CGI365Lib as CGI

# get_image.cgi
req, res = (CGI.Request(), CGI.Response())

path = req.getParam("path")
res.sendImage(path)