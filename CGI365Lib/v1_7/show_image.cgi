#!D:/python312/python.exe
import CGI365Lib as CGI

# show_image.html
req, res = (CGI.Request(), CGI.Response())

html = "./html/show_image.html"
res.sendHtml(html)
