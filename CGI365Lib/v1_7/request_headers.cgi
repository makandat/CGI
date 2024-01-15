#!D:/python312/python.exe
import CGI365Lib as CGI

req, res = (CGI.Request(), CGI.Response())
headers_list = list()
for k in req.Headers.keys():
    headers_list.append(f"{k}: {req.Headers[k]}")
html_list = CGI.Utility.htmlList(headers_list)

res.sendHtml("./templates/request_headers.html", embed={"html_list":html_list, "title":"HTTP Headers"})
