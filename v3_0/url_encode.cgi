#!C:/Python3/python.exe
import urllib.parse as urlp
import CGI365Lib as CGI

# Start
req, res = (CGI.Request(), CGI.Response())

url = req.getParam("url");
q = urlp.quote(url)
res.sendSimple(q, "utf-8")
