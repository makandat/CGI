#!D:/python312/python.exe
import CGI365Lib as CGI
import SQLite3

# POST method
def onPOST(req, res):
  param = req.parseJSON()
  db = param["db"]
  sql = param["sql"]
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
def onGET(req, res):
  htmlfile = "./html/post_json.html"
  res.sendHtml(htmlfile)
  return

# Start
req, res = (CGI.Request(), CGI.Response())

if req.Method == "POST":
  onPOST(req, res)
else:
  onGET(req, res)
