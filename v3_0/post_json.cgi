#!C:/Python3/python.exe
import CGI365Lib as CGI
import SQLite3

# POST method
def on_POST(req, res):
  db = req.getParam("db")
  sql = req.getParam("sql")
  if db == "" or sql == "":
    res.sendJSON({"message":CGI.BAD_REQUEST, "table":""})
    return
  try:
    CGI.info(db)
    CGI.info(sql)
    resultset = SQLite3.query(db, sql)
    CGI.info("query OK")
    table = CGI.Utility.htmlTable(resultset, header=False, table="table striped")
  except:
    res.sendJSON({"message":CGI.INTERNAL_SERVER_ERROR, "table":""})
    return
  res.sendJSON({"message":"OK", "table":table})
  return

# GET method
def on_GET(req, res):
  htmlfile = "./html/post_json.html"
  res.sendHtml(htmlfile)
  return

# Start
if __name__ == "__main__":
  req, res = (CGI.Request(), CGI.Response())

  if req.method == "POST":
    on_POST(req, res)
  elif req.method == "GET":
    on_GET(req, res)
  else:
    CGI.Response.status(405, CGI.METHOD_NOT_ALLOWED)
