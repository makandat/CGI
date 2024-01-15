#!D:/python312/python.exe
import CGI365Lib as CGI

req, res = (CGI.Request(), CGI.Response())

html = "./html/index.html"
res.sendHtml(html)

