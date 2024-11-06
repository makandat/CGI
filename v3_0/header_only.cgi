#!C:/Python3/python.exe
import CGI365Lib as CGI

req, res = (CGI.Request(), CGI.Response())

# クッキーを削除する。
cookie_name = req.getParam("cookie_name")
headers = ["Set-Cookie: " + cookie_name +"= ;Max-Age=0"]
CGI.Response.header(headers)
