#!D:/python312/python.exe
import CGI365Lib as CGI

req, res = (CGI.Request(), CGI.Response())

message = req.getParam("message")
html = "./templates/echo.html"
res.sendHtml(html, embed={"message":message})
