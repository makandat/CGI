#!D:/python312/python.exe
import CGI365Lib as CGI

req, res = (CGI.Request(), CGI.Response())
cookie_list = list()
for k, v in req.Cookies.items():
  cookie_list.append(f"{k}: {v}")
html_list = CGI.Utility.htmlList(cookie_list)

res.sendHtml("./templates/request_cookies.html", embed={"html_list":html_list, "title":"HTTP Request Cookies"})
