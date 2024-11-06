#!C:/Python3/python.exe
import CGI365Lib as CGI

SAVEFILE = "C:/temp/save_www_data.txt"

# ファイル保存
def saveFile(headers, data):
  f = open(SAVEFILE, "w")
  f.write(headers + "\n" + data)
  f.close()
  return

# GET method
def on_GET(req, res):
  headers = ""
  data = ""
  if req.queryString != None:
    for k, v in req.headers.items():
      headers += k + ": " + v + "\n"
    data = req.queryString.replace("\r", "")
    saveFile(headers, data)
  res.sendHtml("./html/save_www_data.html", embed={"headers":headers, "data":data, "message":f"{SAVEFILE} に全データを保存しました。"})
  return

# POST method
def on_POST(req, res):
  headers = ""
  for k, v in req.headers.items():
    headers += k + ": " + v + "\n"
  data = req.body.decode().replace("\r", "")
  res.sendHtml("./html/save_www_data.html", embed={"headers":headers, "data":data, "message":f"{SAVEFILE} に全データを保存しました。"})
  saveFile(headers, data)
  return

# Start
if __name__ == '__main__':
  req, res = (CGI.Request(), CGI.Response())
  if req.method == "GET":
    on_GET(req, res)
  elif req.method == "POST":
    on_POST(req, res)
  else:
    CGI.Response.status(405, CGI.METHOD_NOT_ALLOWED)
