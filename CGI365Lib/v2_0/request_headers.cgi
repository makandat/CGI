#!D:/python312/python.exe
import CGI365Lib as CGI

HTML = "./templates/request_headers.html"

def on_GET(req, res):
  headers_list = list()
  for k in req.headers.keys():
    headers_list.append(f"{k}: {req.headers[k]}")
  html_list = CGI.Utility.htmlList(headers_list, ul="ms-5")
  res.sendHtml(HTML, embed={"html_list":html_list, "title":"HTTP Headers"})
  return

# Main
if __name__ == "__main__":
  req, res = (CGI.Request(), CGI.Response())
  if req.method == "GET":
    on_GET(req, res)
  else:
    CGI.Response.status(405, METHOD_NOT_ALLOWED)
