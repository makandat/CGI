#!C:/Python3/python.exe
import CGI365Lib as CGI
import MariaDB as maria

req, res = (CGI.Request(), CGI.Response())

criteria = req.getParam("criteria")

sql = "SELECT id, album, title, creator, path, media, mark, info, fav, date FROM Pictures"
if len(criteria) > 0:
  sql += f" WHERE {criteria}"
db = maria.MariaDB()
resultset = db.query(sql)

table = "<table class=\"table\">\n"
table += "<tr><th>id</th><th>album</th><th>title</th><th>creator</th><th>path</th><th>media</th><th>mark</th><th>info</th><th>fav</th><th>date</th></tr>\n"
for row in resultset:
  table += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td><td>{row[5]}</td><td>{row[6]}</td><td>{row[7]}</td><td>{row[8]}</td><td>{row[9]}</td></tr>\n"
table += "</table>\n" 
res.sendString(table)
