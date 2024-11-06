#!C:/Python3/python.exe
import CGI365Lib as CGI
import MariaDB as maria

req, res = (CGI.Request(), CGI.Response())

id = req.getParam("id")
sql = f"SELECT album, title, creator, path, media, mark, info, fav, date FROM Pictures WHERE id={id}"
db = maria.MariaDB()

n = db.getValue(f"SELECT count(id) AS n FROM Pictures WHERE id={id}")
if n == 0:
  res.sendJSON({"message":"Error: This id does not exists."})
else:
  result = db.getRow(sql)
  date = str(result[8])
  data = {"message":"OK", "id":id, "album":result[0], "title":result[1], "creator":result[2],
  "path":result[3], "media":result[4], "mark":result[5], "info":result[6], "fav":result[7], "date":date}
  res.sendJSON(data)
