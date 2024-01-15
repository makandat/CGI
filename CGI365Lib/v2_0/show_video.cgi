#!D:/python312/python.exe
import CGI365Lib as CGI

req, res = (CGI.Request(), CGI.Response())

html = "./html/show_video.html"
res.sendHtml(html)
