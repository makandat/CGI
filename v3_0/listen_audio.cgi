#!C:/Python3/python.exe
import CGI365Lib as CGI

req, res = (CGI.Request(), CGI.Response())

html = "./html/listen_audio.html"
res.sendHtml(html)
